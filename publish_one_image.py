import os
import telegram
import random
import argparse
import sys
from dotenv import load_dotenv


def pick_random_image():
    images = []
    for root, dirs, files in os.walk("images"):
        for name in files:
            images.append(os.path.join(root, name))
    if not images:
        return None
    return random.choice(images)


def create_parser():
    parser = argparse.ArgumentParser(
        description="Программа для публикации одного конкретного или случайного изображения в Telegram"
    )
    parser.add_argument(
        "-i",
        "--image_path",
        help="Путь к конкретному изображению. Если не указан, берется случайное изображение из папки 'images'.",
        default=None,
    )

    return parser


def publish_photo_tg_bot(bot, chat_id, image_path):
    with open(image_path, 'rb') as photo_file:
        bot.send_photo(
            chat_id=chat_id,
            photo=photo_file,
            )


def main():
    load_dotenv(".env")
    tg_token = os.getenv("TG_SPACE_TOKEN")
    bot = telegram.Bot(token=tg_token)
    tg_channel_id = os.getenv("TG_CHANNEL")
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    image_path = namespace.image_path
    if not image_path:
        image_path = pick_random_image()
    if not image_path:
        print("Ошибка: Не указан путь к файлу, а папка 'images' пуста или отсутствует.")
        return
    publish_photo_tg_bot(bot=bot, chat_id=tg_channel_id, image_path=image_path)


if __name__ == "__main__":
    main()
