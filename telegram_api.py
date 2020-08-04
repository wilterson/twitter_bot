import credentials
import telepot


class TelegramApi():
    def __init__(self):
        self.chat_id = credentials.CHAT_ID
        self.bot = telepot.Bot(credentials.TELEGRAM_TOKEN)

    def send_message(self, message):
        self.bot.sendMessage(self.chat_id, message)
