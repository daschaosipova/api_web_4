import requests
import sys
import argparse
from dotenv import load_dotenv
from pathlib import Path
from download_helpers import download_image

load_dotenv(".env")


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-id", "--launch_id", help="id Запуска", default="latest"
    )

    return parser


def fetch_spacex_last_launch(launch_id):
    response = requests.get(
        f"https://api.spacexdata.com/v5/launches/{launch_id}"
    )
    response.raise_for_status()
    images_urls = response.json()["links"]["flickr"]["original"]
    folder = Path("images")
    folder.mkdir(parents=True, exist_ok=True)

    for url_number, url in enumerate(images_urls):
        filename = f"spacex{url_number}.jpeg"
        filepath = folder / filename
        download_image(url, filepath=filepath)


def main():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    launch_id = namespace.launch_id
    fetch_spacex_last_launch(launch_id=launch_id)


if __name__ == "__main__":
    main()
