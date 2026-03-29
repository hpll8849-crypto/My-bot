import os
import re
import requests
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# --- إعداد السيرفر لـ Render ---
app = Flask('')
@app.route('/')
def home(): return "UserBot is Alive!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعداد الحساب (UserBot) ---
# استبدل هذه القيم بالتي استخرجتها من my.telegram.org
api_id = 1234567  # ضع الـ api_id الخاص بك هنا
api_hash = "your_api_hash_here" # ضع الـ api_hash الخاص بك هنا
# التوكن الخاص بالبوت الذي أنشأته سابقاً
bot_token = "7695684640:AAHisgNStN12mWy_qVyXtf3h7XUuMOhIYj0"

app_bot = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app_bot.on_message(filters.text & filters.private)
async def download_and_send(client, message):
    urls = re.findall(r'(https?://[^\s]+)', message.text)
    if not urls: return

    status = await message.reply("⏳ جاري التحميل والرفع (يدعم حتى 2 جيجا)...")

    for url in urls:
        try:
            filename = f"video_{message.id}.mp4"
            # تحميل الفيديو إلى سيرفر Render مؤقتاً
            response = requests.get(url, stream=True)
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # الرفع كحساب (يتجاوز 50 ميجا)
            await client.send_video(message.chat.id, filename, caption="✅ جودة أصلية (200MB+)")
            os.remove(filename)
        except Exception as e:
            await message.reply(f"❌ خطأ: {str(e)}")

    await status.delete()

if __name__ == "__main__":
    keep_alive()
    print("UserBot started!")
    app_bot.run()
