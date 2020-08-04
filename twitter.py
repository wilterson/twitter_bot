import random
import tweepy
import time
import os
import logging
from ritetag_api import RiteTag
import credentials


class TwitterBot:

    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        auth = tweepy.OAuthHandler(
            credentials.TWEEPY_KEY, credentials.TWEEPY_SECRET)

        auth.set_access_token(credentials.TWEEPY_ACCESS_KEY,
                              credentials.TWEEPY_ACCESS_SECRET)

        self.ritetag_api = RiteTag(credentials.RITETAG_TOKEN)

        self.api = tweepy.API(auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True)

        self.user = self.api.me()

    def sleep(self):
        waiting = random.randint(60, 360)
        print('Waiting: ' + str(waiting) + 's \n\n')
        time.sleep(waiting)
        return

    def like_tweet(self, search, number_tweets, follow_author=False):
        for tweet in enumerate(tweepy.Cursor(self.api.search, search).items(number_tweets)):
            try:
                tweet.favorite()
                print('Tweet Liked')
                time.sleep(10)

                if(follow_author):
                    self.follow_user(tweet.user.id)

            except tweepy.TweepError as e:
                logging.warning(e.reason)
            except StopIteration:
                break

    def follow_user(self, user_id):
        self.api.create_friendship(user_id=user_id)
        print('User Followed')
        self.sleep()

    def post_media(self, text='', remove_image=False):
        directory = './images'

        fileDir = os.path.dirname(os.path.realpath('__file__'))

        for filename in os.listdir(directory):
            file = os.path.join(fileDir, f"images/{filename}")
            media = self.api.media_upload(file)

            post = text if len(text) > 0 else 'default text 🙃'

            self.api.update_status(post, media_ids=[media.media_id_string])

            if(remove_image):
                os.remove(file)

            break

    def get_post_text(self, file):
        """ Reads a random line """
        file = open(file, 'r')
        line = next(file)
        for num, lines in enumerate(file, 2):
            if random.randrange(num):
                continue
            line = lines
        return line

    def post_text(self, text):
        stats = self.ritetag_api.get_hashtag_suggestion(text)
        hashtags = "#" + " #".join([stat.hashtag for stat in stats])
        post = text + hashtags
        self.api.update_status(post)
