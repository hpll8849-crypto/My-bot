import os
import re
import requests
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# --- إعداد السيرفر لـ Render (للبقاء حياً 24 ساعة) ---
app = Flask('')

@app.route('/')
def home():
    return "UserBot is Running High Capacity!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات الحساب (بياناتك الخاصة) ---
api_id = 18619009
api_hash = "dbe2d6d5fd80ef0f9869ecb1caaef0df"
bot_token = "7695684640:AAHisgNStN12mWy_qVyXtf3h7XUuMOhIYj0"

# تشغيل البوت بنظام Pyrogram المتطور
app_bot = Client(
    "video_downloader_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

@app_bot.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply("🚀 أهلاً بك! أنا الآن أعمل بنظام الرفع العالي (حتى 2 جيجا).\nأرسل لي أي روابط فيديوهات مباشرة وسأقوم برفعها لك بأعلى جودة.")

@app_bot.on_message(filters.text & filters.private)
async def handle_download(client, message):
    urls = re.findall(r'(https?://[^\s]+)', message.text)
    if not urls:
        return

    status_msg = await message.reply("⏳ جاري التحميل والرفع... قد يستغرق الحجم الكبير بعض الوقت.")

    for url in urls:
        try:
            # اسم الملف مؤقتاً
            filename = f"video_{message.id}.mp4"
            
            # تحميل الفيديو من الرابط إلى سيرفر Render
            response = requests.get(url, stream=True, timeout=300)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024*1024): # تحميل ميجا بميجا
                        if chunk:
                            f.write(chunk)
                
                # رفع الفيديو لتليجرام (هنا تكمن القوة: لا حدود لـ 50 ميجا)
                await client.send_video(
                    chat_id=message.chat.id,
                    video=filename,
                    caption="✅ تم الرفع بأعلى جودة متوفرة",
                    supports_streaming=True # يسمح بمشاهدة الفيديو أثناء التحميل
                )
                
                # حذف الملف المؤقت لتوفير مساحة السيرفر
                if os.path.exists(filename):
                    os.remove(filename)
            else:
                await message.reply(f"❌ فشل الوصول للرابط: {url}")

        except Exception as e:
            await message.reply(f"❌ حدث خطأ مع الرابط: {url}\nالخطأ: {str(e)}")
            if os.path.exists(filename):
                os.remove(filename)

    await status_msg.delete()

if __name__ == "__main__":
    keep_alive()
    print("البوت انطلق بقوة الـ 2 جيجا!")
    app_bot.run()
