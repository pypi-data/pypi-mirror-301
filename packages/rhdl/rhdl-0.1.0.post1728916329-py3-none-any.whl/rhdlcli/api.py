#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
import time

from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from threading import local

from rhdlcli.fs import create_parent_dir
from rhdllib.auth import HmacAuthBase

FIVE_SECONDS = 5
TEN_SECONDS = 10
# We'll allow 5 seconds to connect & 10 seconds to get an answer
REQUESTS_TIMEOUT = (FIVE_SECONDS, TEN_SECONDS)


def build_hmac_context(component_id, base_url, access_key, secret_key):
    class HmacContext(object):
        """
        S3Context builds a request Session() object configured to download
        files from S3 through a redirection from RHDL API.
        """

        def __init__(self, base_url, access_key, secret_key):
            self.threadlocal = local()
            self.session_auth = HmacAuthBase(
                access_key, secret_key, service="api", region="us-east-1"
            )
            self.base_url = base_url

        @property
        def session(self):
            """
            Each thread must have its own `requests.Session()` instance.
            `session` is a property looking for `session` object in a
            thread-local context.
            """
            if not hasattr(self.threadlocal, "session"):
                session = requests.Session()
                session.auth = self.session_auth
                session.stream = True
                self.threadlocal.session = session
            return self.threadlocal.session

        def get(self, relpath):
            return self.session.get(
                "%s/%s" % (self.base_url, relpath.lstrip("/")), timeout=REQUESTS_TIMEOUT
            )

        def head(self, relpath):
            # allow_redirects must be set to True to get the final HTTP status
            return self.session.head(
                "%s/%s" % (self.base_url, relpath.lstrip("/")),
                allow_redirects=True,
                timeout=REQUESTS_TIMEOUT,
            )

    base_url = "%s/api/v1/components/%s/files" % (base_url, component_id)
    return HmacContext(base_url, access_key, secret_key)


def retry(tries=3, delay=2, multiplier=2):
    def decorated_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            _tries = tries
            _delay = delay
            while _tries:
                try:
                    return f(*args, **kwargs)
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print("%s, retrying in %d seconds..." % (str(e), _delay))
                    time.sleep(_delay)
                    _tries -= 1
                    if not _tries:
                        raise
                    _delay *= multiplier
            return f(*args, **kwargs)

        return f_retry

    return decorated_retry


@retry()
def get_files_list(context):
    print("Download file list, it may take a few seconds")
    r = context.get("rhdl_files_list.json")
    r.raise_for_status()
    return r.json()


@retry()
def download_file(context, download_folder, file, i, nb_files):
    start_time = time.monotonic()
    relative_file_path = os.path.join(file["path"], file["name"])
    destination = os.path.join(download_folder, relative_file_path)
    if os.path.exists(destination):
        print(f"({i + 1}/{nb_files}): < Skipping {destination} file already exists")
        return
    print(f"({i + 1}/{nb_files}): < Getting {destination}")
    create_parent_dir(destination)
    r = context.get(relative_file_path)
    r.raise_for_status()
    with open(destination, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)
    download_speed = round(file["size"] / (time.monotonic() - start_time) / 1024, 2)
    print(f"({i + 1}/{nb_files}): > Done {destination} - {download_speed} KB/s")
    return file


def download_files(context, download_folder, files):
    nb_files = len(files)
    with ThreadPoolExecutor(max_workers=10) as executor:
        for file in executor.map(
            download_file,
            *zip(
                *[
                    (context, download_folder, file, i, nb_files)
                    for i, file in enumerate(files)
                ]
            ),
        ):
            pass
