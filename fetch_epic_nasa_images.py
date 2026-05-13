import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from download_helpers import download_image


def fetch_epic_nasa(token, email):
    payload = {"api_key": token}
    all_epic_images = requests.get(
        "https://api.nasa.gov/EPIC/api/natural/all", params=payload
    )
    all_epic_images.raise_for_status()
    last_available_date = all_epic_images.json()[0]["date"]
    year, month, day = last_available_date.split("-")
    response = requests.get(
        f"https://epic.gsfc.nasa.gov/api/natural/date/{year}-{month}-{day}",
        params=payload,
    )
    response.raise_for_status()
    folder = Path("images")
    folder.mkdir(parents=True, exist_ok=True)
    for element in response.json():
        name = f"{element['image']}.png"
        archive = (
            f"https://epic.gsfc.nasa.gov/archive/natural/"
            f"{year}/{month}/{day}/png/"
        )
        image_url = f"{archive}{name}"
        filepath = folder / name
        download_image(image_url, filepath, email)


def main():
    load_dotenv(".env")
    nasa_token = os.getenv("NASA_TOKEN", "DEMO_KEY")
    user_email = os.getenv("EMAIL")
    fetch_epic_nasa(token=nasa_token, email=user_email)


if __name__ == "__main__":
    main()
