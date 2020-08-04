import schedule
from twitter import TwitterBot
import time

bot = TwitterBot()

schedule.every(3).hour.do(bot.like_tweet('#python', 80, follow_author=True))

while True:
    schedule.run_pending()
    time.sleep(1)
