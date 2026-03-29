import os
import telebot
import requests
import re
from flask import Flask
from threading import Thread

# --- إعداد السيرفر ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

def run():
    # Render يستخدم المنفذ 10000 غالباً، لذا سنتركه مرناً
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعداد البوت ---
TOKEN = '7695684640:AAHisgNStN12mWy_qVyXtf3h7XUuMOhIYj0'
bot = telebot.TeleBot(TOKEN)

def extract_urls(text):
    return re.findall(r'(https?://[^\s]+)', text)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🚀 البوت جاهز للتحميل بأعلى جودة!\nأرسل الروابط الآن.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    urls = extract_urls(message.text)
    if not urls:
        return

    msg = bot.reply_to(message, f"⏳ جاري معالجة {len(urls)} رابط...")

    for url in urls:
        try:
            # الإرسال عبر الرابط مباشرة (أفضل وأسرع جودة)
            bot.send_video(message.chat.id, url, caption="✅ تم التحميل بنجاح")
        except Exception:
            bot.send_message(message.chat.id, f"❌ عذراً، لم أستطع تحميل هذا الرابط (قد يكون الحجم أكبر من 50MB):\n{url}")

    bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)

if __name__ == "__main__":
    keep_alive()
    print("Bot is alive and polling...")
    bot.infinity_polling()
