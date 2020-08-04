from ritetag import RiteTagApi


class RiteTag:

    def __init__(self, token):
        self.token = token
        self.client = self.__auth()

    def __auth(self):
        access_token = self.token
        client = RiteTagApi(access_token)
        client.on_limit(80, self.limit_80_percentage_reached)
        return client

    def get_hashtag_suggestion(self, text):
        stats = self.client.hashtag_suggestion_for_text(text)
        return stats

    def limit_80_percentage_reached(self, limit):
        print(f"Used {limit.usage}. The limit resets on {limit.reset}")
