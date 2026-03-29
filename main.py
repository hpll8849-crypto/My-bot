import os
import telebot
import yt_dlp
from flask import Flask
import threading

# 1. إعداد سيرفر ويب لـ Render
app = Flask(__name__)

@app.route('/')
def health_check():
    return "I am alive!", 200

# 2. إعداد البوت (استخدمنا التوكن الخاص بك)
TOKEN = "7695684640:AAHisgNStN12mWy_qVyXtf3h7XUuMOhIYj0"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ البوت يعمل الآن 24/7 على Render!\nأرسل الروابط وسأحاول تحميلها بأعلى جودة.")

@bot.message_handler(func=lambda m: True)
def download_video(message):
    url = message.text
    if "http" not in url:
        return

    wait_msg = bot.reply_to(message, "⏳ جاري المعالجة والتحميل... يرجى الانتظار.")
    
    # إعدادات التحميل بأعلى جودة
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'video_{message.chat.id}.%(ext)s',
        'no_warnings': True,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # التأكد من حجم الملف (تليجرام يسمح للبوت بـ 50MB فقط)
            file_size = os.path.getsize(filename) / (1024 * 1024)
            
            if file_size > 50:
                bot.edit_message_text(f"⚠️ الملف حجمه {file_size:.1f}MB.\nتليجرام يمنع البوتات من إرسال ملفات أكبر من 50MB.\nبإمكانك فتحه مباشرة من المتصفح وحفظه:\n{url}", message.chat.id, wait_msg.message_id)
                os.remove(filename)
            else:
                with open(filename, 'rb') as v:
                    bot.send_video(message.chat.id, v, caption="✅ تم التحميل بأعلى جودة")
                bot.delete_message(message.chat.id, wait_msg.message_id)
                os.remove(filename)

    except Exception as e:
        bot.edit_message_text(f"❌ خطأ: {str(e)}", message.chat.id, wait_msg.message_id)

# دالة لتشغيل البوت في الخلفية
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # تشغيل البوت في خيط (Thread) منفصل
    threading.Thread(target=run_bot, daemon=True).start()
    # تشغيل Flask على المنفذ المطلوب لـ Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
