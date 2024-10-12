# mirrormate/clone.py

import os
import subprocess

def is_wget_installed():
    try:
        subprocess.run(["wget", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def mirror_website(url, silent=False):
    if not is_wget_installed():
        return False
    wget_command = f"wget --mirror --page-requisites --convert-links --no-parent --timestamping {url}"
    if silent:
        os.system(f"{wget_command} > /dev/null 2>&1")
    else:
        os.system(wget_command)
    return True

def download_single_file(file_url, silent=False):
    if not is_wget_installed():
        return False
    wget_command = f"wget {file_url}"
    if silent:
        os.system(f"{wget_command} > /dev/null 2>&1")
    else:
        os.system(wget_command)
    return True

def download_file_format(url, file_format, silent=False):
    if not is_wget_installed():
        return False
    wget_command = f"wget -r -l1 -A {file_format} {url}"
    if silent:
        os.system(f"{wget_command} > /dev/null 2>&1")
    else:
        os.system(wget_command)
    return True

def clone(url=None, file_url=None, file_format=None, silent=False):
    if url:
        return mirror_website(url, silent)
    elif file_url:
        return download_single_file(file_url, silent)
    elif file_format and url:
        return download_file_format(url, file_format, silent)
    return False
