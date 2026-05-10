import os
import requests
import argparse
import sys
from dotenv import load_dotenv
from pathlib import Path
from download_helpers import download_image, define_image_extension

load_dotenv(".env")


def create_parser():
    parser = argparse.ArgumentParser()
    images_count = os.getenv("IMAGES_COUNT_NASA", 50)
    parser.add_argument(
        "-c",
        "--images_count",
        help="Количество фото для скачивания",
        type=int,
        default=int(images_count),
    )

    return parser


def fetch_apod_nasa(token, count):
    payload = {"count": count, "api_key": token}
    response = requests.get(
        "https://api.nasa.gov/planetary/apod", params=payload
    )
    images_urls = []
    for element in response.json():
        image_url = element["url"]
        images_urls.append(image_url)
    folder = Path("images")
    folder.mkdir(parents=True, exist_ok=True)
    for image_url_number, image_url in enumerate(images_urls):
        extension = define_image_extension(image_url)
        filename = f"nasa_apod_{image_url_number}{extension}"
        filepath = folder / filename
        download_image(image_url, filepath)


def main():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    images_count = namespace.images_count
    fetch_apod_nasa(token=os.getenv("NASA_TOKEN","DEMO_KEY"), count=images_count)


if __name__ == "__main__":
    main()
