from telegram import Bot
import os
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def test():
    bot = Bot(BOT_TOKEN)
    me = await bot.get_me()
    print("✅ Bot username:", me.username)

asyncio.run(test())
