import os
import telegram
import time
import random
import argparse
import sys
from dotenv import load_dotenv


load_dotenv(".env")


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--frequency",
        help="Частота публикации фото в секундах",
        default=14400,
        type=int,
    )

    return parser


def post_photo_tg_bot(bot, chat_id, frequency):
    images = []
    for root, dirs, files in os.walk("images"):
        for name in files:
            images.append(os.path.join(root, name))
    if not images:
        print("Ошибка: папка 'images' пуста или не найдена.")
        return
    while True:
        random.shuffle(images)
        for image_path in images:
            with open(image_path, "rb") as photo_file:
                bot.send_photo(
                    chat_id=chat_id,
                    photo=photo_file,
                )
            time.sleep(frequency)


def main():
    tg_token = os.getenv("TG_SPACE_TOKEN")
    bot = telegram.Bot(token=tg_token)
    tg_channel_id = os.getenv("TG_CHANNEL")
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    frequency = namespace.frequency
    try:
        post_photo_tg_bot(bot, tg_channel_id, frequency)
    except KeyboardInterrupt:
        print("\nПубликация остановлена пользователем.")


if __name__ == "__main__":
    main()
