import telebot
import os

TOKEN = "7695684640:AAHisgNStN12mWy_qVyXtf3h7XUuMOhIYj0" # ضعه مباشرة للتجربة
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, "البوت شغال وعم يسمعك!")

print("Started...")
bot.infinity_polling()
