import settings
import telebot
from telebot import types

bot = telebot.TeleBot(settings.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text=message.message_id)

if __name__ == "__main__":
    bot.polling(none_stop=True)
