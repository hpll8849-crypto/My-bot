import os
import re
import asyncio
import requests
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "UserBot is Running!", 200

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

app_user = Client(
    "my_account",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

@app_user.on_message(filters.text & filters.private)
async def handle_download(client, message):
    urls = re.findall(r'(https?://[^\s]+)', message.text)
    if not urls:
        return

    status = await message.reply("⏳ جاري سحب الفيديو ورفعه...")
    file_name = f"video_{message.id}.mp4"

    try:
        url = urls[0]
        with requests.get(url, stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

        await client.send_video(
            chat_id=message.chat.id,
            video=file_name,
            caption="✅ تم التحميل بالجودة الأصلية",
            supports_streaming=True
        )
        await status.delete()

    except Exception as e:
        await status.edit(f"❌ حدث خطأ: {str(e)}")

    finally:
        if os.path.exists(file_name):
            os.remove(file_name)

def run_pyrogram():
    # ننشئ event loop جديد خاص بـ Pyrogram لأن Python 3.10+ لا ينشئه تلقائياً
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app_user.run()

if __name__ == "__main__":
    Thread(target=run_pyrogram, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
