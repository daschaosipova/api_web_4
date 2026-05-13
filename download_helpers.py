import os
import requests
import urllib.parse
from urllib.parse import urlsplit


def define_image_extension(url):
    parsed_url = urlsplit(url)
    root, extension = os.path.splitext(urllib.parse.unquote(parsed_url.path))
    return extension


def download_image(url, filepath, email):
    headers = {
        "User-Agent": f"MyCoolApp/1.0 ({email}) Python-requests/2.31"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    with open(filepath, "wb") as file:
        file.write(response.content)
