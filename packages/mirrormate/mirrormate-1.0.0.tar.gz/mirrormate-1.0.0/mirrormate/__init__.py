"""
MirrorMate - A simple command-line tool for mirroring websites and downloading files.

Author: Your Name
Copyright (c) 2024 Your Name. All rights reserved.
"""

from .clone import mirror_website, download_single_file

def clone(url=None, file_url=None, silent=False):
    if url:
        return mirror_website(url, silent)
    elif file_url:
        return download_single_file(file_url, silent)
    return False
