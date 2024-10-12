import os
import subprocess
import requests
from bs4 import BeautifulSoup

def is_wget_installed():
    try:
        subprocess.run(["wget", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def fetch_robots_txt(base_url):
    try:
        robots_url = os.path.join(base_url, "robots.txt")
        response = requests.get(robots_url)
        if response.status_code == 200:
            return response.text
        return ""
    except Exception:
        return ""

def parse_robots_txt(robots_txt):
    disallowed_paths = []
    for line in robots_txt.splitlines():
        line = line.strip()
        if line.startswith("Disallow:"):
            path = line.split(":")[1].strip()
            disallowed_paths.append(path)
    return disallowed_paths

def is_path_allowed(url, disallowed_paths):
    for disallowed in disallowed_paths:
        if url.startswith(disallowed):
            return False
    return True

def get_disallowed_paths(base_url):
    robots_txt = fetch_robots_txt(base_url)
    if robots_txt:
        return parse_robots_txt(robots_txt)
    return []

def mirror_website(url, silent=False):
    if not is_wget_installed():
        return False

    base_url = '/'.join(url.split('/')[:3])  # Extracting the base URL
    disallowed_paths = get_disallowed_paths(base_url)
    
    if not is_path_allowed(url, disallowed_paths):
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
    
    base_url = '/'.join(file_url.split('/')[:3])
    disallowed_paths = get_disallowed_paths(base_url)

    if not is_path_allowed(file_url, disallowed_paths):
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
    
    base_url = '/'.join(url.split('/')[:3])
    disallowed_paths = get_disallowed_paths(base_url)

    if not is_path_allowed(url, disallowed_paths):
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
