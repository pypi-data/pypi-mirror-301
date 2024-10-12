import os
import subprocess

def mirror_website(url, silent=False):
    wget_command = f"wget --mirror --page-requisites --convert-links --no-parent {url}"
    if silent:
        subprocess.run(wget_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run(wget_command, shell=True)
    return os.path.exists(url.split('/')[-1])  # Check if the folder for the URL exists

def download_single_file(file_url, silent=False):
    wget_command = f"wget {file_url}"
    if silent:
        subprocess.run(wget_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run(wget_command, shell=True)
    return os.path.exists(file_url.split('/')[-1])  # Check if the file has been downloaded
