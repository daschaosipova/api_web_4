import os
import requests
import argparse
import sys
from dotenv import load_dotenv
from pathlib import Path
from download_helpers import download_image, define_image_extension


def create_parser(images_count):
    parser = argparse.ArgumentParser(
        description="Программа для автоматического скачивания астрономических картинок дня (APOD) с сайта NASA."
    )
    parser.add_argument(
        "-c",
        "--images_count",
        help="Количество фотографий, которое необходимо скачать (по умолчанию: %(default)s)",
        type=int,
        default=int(images_count),
    )

    return parser


def fetch_apod_nasa(token, count, email):
    payload = {"count": count, "api_key": token}
    response = requests.get(
        "https://api.nasa.gov/planetary/apod", params=payload
    )
    response.raise_for_status()
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
        download_image(image_url, filepath, email)


def main():
    load_dotenv(".env")
    nasa_token = os.getenv("NASA_TOKEN", "DEMO_KEY")
    user_email = os.getenv("EMAIL")
    env_images_count = os.getenv("IMAGES_COUNT_NASA", 50)
    parser = create_parser(images_count=env_images_count)
    namespace = parser.parse_args(sys.argv[1:])
    images_count = namespace.images_count
    fetch_apod_nasa(
        token=nasa_token,
        count=images_count,
        email=user_email,
    )


if __name__ == "__main__":
    main()
