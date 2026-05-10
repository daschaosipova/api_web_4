import os
import telegram
import time
import random
import argparse
import sys
from dotenv import load_dotenv


load_dotenv(".env")


def pick_random_image():
    images = []
    for root, dirs, files in os.walk("images"):
        for name in files:
            images.append(os.path.join(root, name))
    if not images:
        print("Ошибка: папка 'images' пуста или не найдена.")
        return
    image_path = random.choice(images)
    return image_path


def create_parser(image_path):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--image_path",
        help="Название и путь до фото",
        default=image_path,
    )

    return parser


def publish_photo_tg_bot(bot, chat_id, image_path):
    with open(image_path, 'rb') as photo_file:
        bot.send_photo(
            chat_id=chat_id,
            photo=photo_file,
            )


def main():
    tg_token = os.getenv("TG_SPACE_TOKEN")
    bot = telegram.Bot(token=tg_token)
    tg_channel_id = os.getenv("TG_CHANNEL")
    parser = create_parser(pick_random_image())
    namespace = parser.parse_args(sys.argv[1:])
    image_path = namespace.image_path
    publish_photo_tg_bot(bot=bot, chat_id=tg_channel_id, image_path=image_path)


if __name__ == "__main__":
    main()
