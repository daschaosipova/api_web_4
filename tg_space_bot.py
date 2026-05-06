import os
import telegram
from dotenv import load_dotenv

load_dotenv(".env")


def main():
    tg_token = os.getenv('TG_SPACE_TOKEN')
    bot = telegram.Bot(token=tg_token)
    tg_channel_id = os.getenv('TG_CHANNEL')
    bot.send_message(chat_id=tg_channel_id, text='Пристегните ремни, мы начинаем!')
    with open('images/nasa_apod_24.jpg', 'rb') as photo_file:
        bot.send_photo(
            chat_id=tg_channel_id,
            photo=photo_file,
            )


if __name__ == "__main__":
    main()
