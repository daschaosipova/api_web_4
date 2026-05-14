import requests
import sys
import argparse
from dotenv import load_dotenv
from pathlib import Path
from download_helpers import download_image


def create_parser():
    parser = argparse.ArgumentParser(description="Программа для автоматического скачивания фотография ракетного запуска с сайта SpaceX.")
    parser.add_argument(
        "-id",
        "--launch_id",
        help="id Запуска, фотографии которого необходимо скачать (последний запуск по умолчанию)",
        default="latest",
    )

    return parser


def fetch_spacex_last_launch(launch_id, email):
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
        download_image(url, filepath=filepath, email)


def main():
    load_dotenv(".env")
    user_email = os.getenv("EMAIL")
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    launch_id = namespace.launch_id
    fetch_spacex_last_launch(launch_id=launch_id, email=user_email)


if __name__ == "__main__":
    main()
