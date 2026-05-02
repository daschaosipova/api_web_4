import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from download_helpers import download_image, define_image_extension

load_dotenv(".env")


def fetch_apod_nasa(token="DEMO_KEY", count=50):
    payload = {"count": count, "api_key": token}
    response = requests.get(
        "https://api.nasa.gov/planetary/apod", params=payload
    )
    images_urls = []
    for element in response.json():
        image_url = element["url"]
        images_urls.append(image_url)
    folder = Path("images_nasa")
    folder.mkdir(parents=True, exist_ok=True)
    for image_url_number, image_url in enumerate(images_urls):
        extension = define_image_extension(image_url)
        filename = f"nasa_apod_{image_url_number}{extension}"
        filepath = folder / filename
        download_image(image_url, filepath)


def main():
    fetch_apod_nasa(token=os.environ["NASA_TOKEN"], count=30)


if __name__ == "__main__":
    main()
