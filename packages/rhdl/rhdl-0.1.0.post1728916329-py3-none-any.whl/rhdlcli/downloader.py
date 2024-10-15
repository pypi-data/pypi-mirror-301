#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from rhdlcli.api import (
    get_files_list,
    download_files,
    build_hmac_context,
)
from rhdlcli.stats import check_download_folder_has_enough_space
from rhdlcli.files import get_files_to_remove, filter_files
from rhdlcli.fs import (
    mkdir_p,
    delete_all_symlink_in_path,
    recreate_symlinks,
)


def clean_download_folder(download_folder, files):
    print("Verifying local mirror, this may take some time")

    if not os.path.isdir(download_folder):
        mkdir_p(download_folder)

    for file in get_files_to_remove(download_folder, files):
        print(f"Remove file {file}")
        os.remove(file)

    delete_all_symlink_in_path(download_folder)


def download_component(options):
    context = build_hmac_context(
        component_id=options["compose_id"],
        base_url=options["base_url"],
        access_key=options["access_key"],
        secret_key=options["secret_key"],
    )
    files_list = get_files_list(context)

    files = files_list["files"]
    files = filter_files(files, options["include_and_exclude"])

    download_folder = options["destination"]
    clean_download_folder(download_folder, files)
    check_download_folder_has_enough_space(download_folder, files)

    download_files(context, download_folder, files)

    recreate_symlinks(download_folder, files_list["symlinks"])
