import os
import telebot
import requests
import re
from flask import Flask
from threading import Thread

# --- إعداد السيرفر لضمان استمرارية التشغيل على Render ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعداد البوت ---
# ملاحظة: سأضع التوكن هنا مباشرة لضمان عمله معك فوراً دون إعدادات إضافية
TOKEN = '7695684640:AAHisgNStN12mWy_qVyXtf3h7XUuMOhIYj0'
bot = telebot.TeleBot(TOKEN)

def extract_urls(text):
    # استخراج الروابط التي تنتهي بـ mp4 أو روابط تويتر المباشرة
    return re.findall(r'(https?://[^\s]+)', text)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🚀 أهلاً بك! أنا الآن جاهز للتحميل.\n\nأرسل لي أي روابط فيديوهات (مباشرة) وسأقوم بإرسالها لك فوراً بأعلى جودة متوفرة.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    urls = extract_urls(message.text)
    
    if not urls:
        bot.reply_to(message, "❌ لم أجد روابط في رسالتك. تأكد من إرسال رابط فيديو مباشر.")
        return

    processing_msg = bot.reply_to(message, f"⏳ جاري معالجة {len(urls)} رابط... يرجى الانتظار.")

    for url in urls:
        try:
            # محاولة إرسال الفيديو عبر الرابط مباشرة (أسرع وأعلى جودة)
            bot.send_video(
                message.chat.id, 
                url, 
                caption="✅ تم التحميل بأعلى جودة",
                reply_to_message_id=message.message_id
            )
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ فشل تحميل هذا الرابط:\n{url}\n\nالسبب: قد يكون الحجم أكبر من 50 ميجا أو الرابط غير مدعوم.")

    bot.delete_message(chat_id=message.chat.id, message_id=processing_msg.message_id)

if __name__ == "__main__":
    keep_alive()
    print("البوت انطلق!")
    bot.infinity_polling()
