import os
import re
import requests
import asyncio
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# --- سيرفر صغير لـ Render ---
app = Flask(__name__)
@app.route('/')
def home(): return "UserBot is Active!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- إعدادات الحساب ---
API_ID = 18619009
API_HASH = "dbe2d6d5fd80ef0f9869ecb1caaef0df"
# ضع الـ Session String الخاص بك هنا
SESSION_STRING = "BAEcGoEAIxpn6rkachNa29Gk-IHspGRr6YAM11Zrcy4xuJkubDKB0bYy2TVGPEcU8yvUjMt53RIka-BfXa7IH2Q4MudTyOBDwDXdelDT3cMHYJA6Hz5pjwDRE-KSnN4zROAw7wdvN0toij7DawqXLcs5HbuBVdvLNzGzYLjzIAKWgH6K65F2pzbL8b4ISbNjJ1GMIq0gF2snVC0yW_3M0bOl4W3b1Jc2d2x0L4YcveiZ8NUQbM9TjFRTv1cYERe4mywupaJBa4uiDIXKz_dohIUjJ-xVbGY4BdrZdgzVBq8jLv9X9z5FRzp2qnTdCZiYUShGM4REYcABy84SP7uQq-ARH349mQAAAAGhYRnzAA"

async def start_bot():
    app_user = Client(
        "my_account",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION_STRING,
        in_memory=True
    )

    @app_user.on_message(filters.text & filters.private)
    async def handle_download(client, message):
        urls = re.findall(r'(https?://[^\s]+)', message.text)
        if not urls: return
        
        status = await message.reply("⏳ جاري سحب الفيديو ورفعه (دعم حتى 2 جيجا)...")
        
        try:
            file_name = f"video_{message.id}.mp4"
            with requests.get(urls[0], stream=True) as r:
                r.raise_for_status()
                with open(file_name, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024*1024):
                        f.write(chunk)
            
            await client.send_video(message.chat.id, file_name, caption="✅ تم التحميل بحجم كامل")
            if os.path.exists(file_name): os.remove(file_name)
            await status.delete()
        except Exception as e:
            await status.edit(f"❌ خطأ: {str(e)}")

    print("جاري تشغيل البوت...")
    await app_user.start()
    # كود لمنع التوقف (إبقاء البوت حياً)
    while True:
        await asyncio.sleep(1000)

if __name__ == "__main__":
    # تشغيل Flask في الخلفية
    Thread(target=run_flask, daemon=True).start()
    
    # تشغيل البوت بطريقة تتوافق مع إصدارات بايثون الجديدة
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(start_bot())
    except KeyboardInterrupt:
        pass
