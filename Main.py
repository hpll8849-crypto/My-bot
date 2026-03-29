import telebot
import requests
import re
import os
import subprocess
from urllib.parse import urlparse

# التوكن الخاص بك
TOKEN = '7695684640:AAHisgNStN12mWy_qVyXtf3h7XUuMOhIYj0'
bot = telebot.TeleBot(TOKEN)

def extract_urls(text):
    return re.findall(r'(https?://[^\s]+)', text)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🚀 البوت يعمل الآن على استضافة دائمية!\nأرسل الروابط وسأقوم بتحميلها بأعلى جودة.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    urls = extract_urls(message.text)
    if not urls:
        return

    status_msg = bot.reply_to(message, f"⏳ جاري معالجة {len(urls)} فيديو...")

    for url in urls:
        try:
            # محاولة الإرسال السريع عبر الرابط أولاً
            bot.send_video(message.chat.id, url, caption="تم الرفع السريع ⚡️")
        except:
            # إذا فشل، يتم التحميل عبر yt-dlp لجلب أعلى جودة
            try:
                filename = f"vid_{os.urandom(4).hex()}.mp4"
                # تحميل أعلى جودة مدمجة (فيديو + صوت)
                cmd = f'yt-dlp -f "bestvideo+bestaudio/best" --merge-output-format mp4 "{url}" -o {filename}'
                subprocess.run(cmd, shell=True)

                if os.path.exists(filename):
                    with open(filename, 'rb') as v:
                        bot.send_video(message.chat.id, v, caption="تم التحميل بأعلى جودة ✅")
                    os.remove(filename)
            except Exception as e:
                bot.send_message(message.chat.id, f"❌ خطأ في الرابط: {url}\n{str(e)}")

    bot.delete_message(chat_id=status_msg.chat.id, message_id=status_msg.message_id)

if __name__ == "__main__":
    print("البوت انطلق...")
    bot.infinity_polling()
