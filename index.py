import schedule
from twitter import TwitterBot
import time
from telegram_api import TelegramApi
import logging
import threading


def init_logging():
    logging.basicConfig(
        format="%(asctime)s : %(levelname)s : %(message)s",
        filename="app.log",
        filemode="w",
        level=logging.INFO,
    )


def run_threaded(job):
    job_thread = threading.Thread(target=job)
    job_thread.start()


init_logging()
bot = TwitterBot()

schedule.every().day.at("09:00").do(bot.post_text, text="Good Morning Twitter!")

while True:
    schedule.run_pending()
    time.sleep(1)
