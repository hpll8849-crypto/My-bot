import os
import telebot
import requests
import re
from flask import Flask
from threading import Thread

# --- إعداد السيرفر لـ Render ---
app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل الآن بنجاح!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- كود البوت ---
TOKEN = os.environ.get('BOT_TOKEN') # سنجلب التوكن من إعدادات Render للأمان
bot = telebot.TeleBot(TOKEN)

def extract_urls(text):
    return re.findall(r'(https?://[^\s]+)', text)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🚀 بوت التحميل المستمر من Render يعمل الآن!\nأرسل الروابط وسأقوم بالتحميل بأعلى جودة.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    urls = extract_urls(message.text)
    if not urls: return
    
    msg = bot.reply_to(message, f"🔄 جاري المعالجة... (العدد: {len(urls)})")
    
    for url in urls:
        try:
            # محاولة الإرسال المباشر (الأسرع وتتجاوز الحجم غالباً)
            bot.send_video(message.chat.id, url, caption="تم الرفع بنجاح ⚡️")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ فشل الرابط: {url}\nتأكد أن الملف لا يتجاوز 50 ميجا.")

    bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)

if __name__ == "__main__":
    keep_alive() # تشغيل السيرفر في الخلفية
    print("Bot is running...")
    bot.infinity_polling()
