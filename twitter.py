import random
import tweepy
import time
import os
import logging
from ritetag_api import RiteTag
from telegram_api import TelegramApi
import credentials


class TwitterBot:
    def __init__(self):
        auth = tweepy.OAuthHandler(credentials.TWEEPY_KEY, credentials.TWEEPY_SECRET)

        auth.set_access_token(
            credentials.TWEEPY_ACCESS_KEY, credentials.TWEEPY_ACCESS_SECRET
        )

        self.telegram = TelegramApi()

        self.ritetag_api = RiteTag(credentials.RITETAG_TOKEN)

        self.api = tweepy.API(
            auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True
        )

        self.user = self.api.me()

    def sleep(self):
        waiting = random.randint(60, 360)
        logging.info(f"Waiting: {str(waiting)}s")
        time.sleep(waiting)
        return

    def like_tweet(self, search, number_tweets=50, follow_author=False):
        for tweet in enumerate(
            tweepy.Cursor(self.api.search, search).items(number_tweets)
        ):
            try:
                tweet.favorite()
                logging.info("Tweet Liked")
                time.sleep(10)

                if follow_author:
                    self.follow_user(tweet.user.id)

            except tweepy.TweepError as e:
                logging.warning(e.reason)
            except StopIteration:
                break

    def follow_user(self, user_id):
        self.api.create_friendship(user_id=user_id)
        logging.info("User Followed")
        self.sleep()

    def post_media(self, text="", remove_media=True):
        """ Post tweet with media attach """
        directory = "./images"

        fileDir = os.path.dirname(os.path.realpath(__file__))

        filename = random.choice(os.listdir(directory))
        file = os.path.join(fileDir, f"images/{filename}")
        media = self.api.media_upload(file)

        post = text if len(text) > 0 else self.get_post_text()

        self.api.update_status(post, media_ids=[media.media_id_string])
        self.telegram.send_message("Tweet postado com sucesso")

        logging.info("Tweet Posted!")

        if remove_media:
            os.remove(file)

    def get_post_text(self):
        """ Reads a random line """
        file = open("posts.txt", "r")
        line = next(file)
        for num, lines in enumerate(file, 2):
            if random.randrange(num):
                continue
            line = lines
        return line

    def post_text(self, text="", auto_hashtag=False):
        """ Post only text tweet"""
        post = text if len(text) > 0 else self.get_post_text()

        if auto_hashtag:
            stats = self.ritetag_api.get_hashtag_suggestion(text)
            hashtags = "#" + " #".join([stat.hashtag for stat in stats])
            post = text + hashtags

        self.api.update_status(post)
        logging.info("Tweet Posted!")
        self.telegram.send_message("Tweet postado com sucesso")

    def unfollow_who_dont_follow_back(self, quantity=50):
        """ Unfollow users who dont follow back """
        for page in tweepy.Cursor(self.api.friends, count=quantity).pages():
            user_ids = [user.id for user in page]

            for relationship in self.api._lookup_friendships(user_ids):
                if not relationship.is_followed_by:
                    logging.info(
                        f"Unfollowing @{relationship.screen_name} ({relationship.id})"
                    )
                    self.sleep()

                    try:
                        self.api.destroy_friendship(relationship.id)
                    except tweepy.error.TweepError as e:
                        logging.error(f"Error unfollowing: {e.reason}")

