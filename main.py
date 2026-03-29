import os
import re
import requests
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# --- إعداد السيرفر لـ Render لضمان عدم التوقف ---
app = Flask(__name__)
@app.route('/')
def home(): return "UserBot High Speed is Running!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- إعدادات الحساب (بياناتك) ---
API_ID = 18619009
API_HASH = "dbe2d6d5fd80ef0f9869ecb1caaef0df"
# ضع النص الطويل جداً بين علامتي التنصيص بالأسفل
SESSION_STRING = "BAEcGoEAIxpn6rkachNa29Gk-IHspGRr6YAM11Zrcy4xuJkubDKB0bYy2TVGPEcU8yvUjMt53RIka-BfXa7IH2Q4MudTyOBDwDXdelDT3cMHYJA6Hz5pjwDRE-KSnN4zROAw7wdvN0toij7DawqXLcs5HbuBVdvLNzGzYLjzIAKWgH6K65F2pzbL8b4ISbNjJ1GMIq0gF2snVC0yW_3M0bOl4W3b1Jc2d2x0L4YcveiZ8NUQbM9TjFRTv1cYERe4mywupaJBa4uiDIXKz_dohIUjJ-xVbGY4BdrZdgzVBq8jLv9X9z5FRzp2qnTdCZiYUShGM4REYcABy84SP7uQq-ARH349mQAAAAGhYRnzAA"

# تشغيل الحساب الشخصي كبوت رفع
app_user = Client("my_account", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

@app_user.on_message(filters.text & filters.private)
async def handle_download(client, message):
    urls = re.findall(r'(https?://[^\s]+)', message.text)
    if not urls: return
    
    status = await message.reply("⏳ جاري سحب الفيديو ورفعه بحجم كامل (يدعم حتى 2 جيجا)...")
    
    try:
        url = urls[0]
        file_name = f"video_{message.id}.mp4"
        
        # تحميل الفيديو للسيرفر
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk: f.write(chunk)
        
        # الرفع كحساب شخصي (يتجاوز 50MB بسهولة)
        await client.send_video(
            chat_id=message.chat.id,
            video=file_name,
            caption="✅ تم التحميل بالجودة الأصلية وحجم كامل",
            supports_streaming=True
        )
        
        if os.path.exists(file_name): os.remove(file_name)
        await status.delete()
        
    except Exception as e:
        await status.edit(f"❌ حدث خطأ أثناء المعالجة: {str(e)}")
        if os.path.exists(file_name): os.remove(file_name)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    print("البوت انطلق بنظام الـ Session!")
    app_user.run()
