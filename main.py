import os
import re
import requests
import asyncio

# --- حل سريع لمشكلة بايثون 3.14 في منصة Render ---
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# --- إعداد السيرفر لـ Render ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive Again!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات الحساب ---
api_id = 18619009
api_hash = "dbe2d6d5fd80ef0f9869ecb1caaef0df"
bot_token = "7695684640:AAHisgNStN12mWy_qVyXtf3h7XUuMOhIYj0"

app_bot = Client("my_video_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app_bot.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply("🚀 أهلاً بك! تم إصلاح العطل وأنا أعمل الآن.")

@app_bot.on_message(filters.text & filters.private)
async def handle_download(client, message):
    urls = re.findall(r'(https?://[^\s]+)', message.text)
    if not urls: return

    status_msg = await message.reply("⏳ جاري المعالجة...")

    for url in urls:
        try:
            # محاولة الإرسال كفيديو مباشر
            await client.send_video(message.chat.id, video=url, caption="✅ تم الرفع")
        except Exception as e:
            # إذا رفض تيليجرام (بسبب الـ 50 ميجا) سيرسل لك الرابط للتحميل/المشاهدة ولن يتعطل
            await message.reply(f"⚠️ الفيديو تجاوز 50MB (حدود البوتات).\nلكن يمكنك مشاهدته وتحميله بأعلى جودة من هنا مباشرة:\n{url}")

    await status_msg.delete()

if __name__ == "__main__":
    keep_alive()
    print("Bot is back online!")
    app_bot.run()
