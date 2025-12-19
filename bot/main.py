import asyncio
import random
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ===== ENV =====
BOT_TOKEN = os.getenv("BOT_TOKEN")

WHATSAPP_GROUP = "https://chat.whatsapp.com/JPA9XEkRReQ3fpzQ7Y4Ldt?mode=hqrt3"
WHATSAPP_CHANNEL = "https://whatsapp.com/channel/0029VbBfAibCxoAtQplkir3Z"

# ===== AUTO UPDATES =====
UPDATE_MESSAGES = [
    "🔴🔵🟣 *LIVE GAME OBSERVATION*\n\n"
    "📊 Aviator showing fast low runs\n"
    "🧠 Best move: *observe & wait*\n\n"
    "⚠️ Blind entry = loss\n"
    "🔔 Stay sharp",

    "📈🟣 *PATTERN MONITOR*\n\n"
    "🔄 Multiple short flights detected\n"
    "💡 Medium spike comes *after patience*\n\n"
    "❌ Don’t chase reds\n"
    "✅ Control emotions",

    "⚠️🔴 *RISK UPDATE*\n\n"
    "📉 High volatility right now\n"
    "💣 Crashes below 2.0x spotted\n\n"
    "🧠 Reduce stake\n"
    "⏳ Timing matters",

    "🧠🔵 *SMART PLAY TIP*\n\n"
    "✔️ Set cashout early\n"
    "✔️ Skip first round after spike\n"
    "❌ No emotional staking\n\n"
    "📌 Discipline wins",

    "📊🟣 *PLAYER BEHAVIOR*\n\n"
    "👥 80% lose by rushing\n"
    "🧠 Calm players last longer\n\n"
    "🔄 Observe → Decide → Enter",

    "📢🔵 *COMMUNITY UPDATE*\n\n"
    f"👉 *WhatsApp Group*: {WHATSAPP_GROUP}\n"
    f"👉 *WhatsApp Channel*: {WHATSAPP_CHANNEL}\n\n"
    "🚀 Stay connected"
]

# ===== BUTTON MENU =====
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📊 Live Signals", callback_data="signals")],
        [InlineKeyboardButton("💬 WhatsApp Group", url=WHATSAPP_GROUP)],
        [InlineKeyboardButton("📢 WhatsApp Channel", url=WHATSAPP_CHANNEL)],
        [InlineKeyboardButton("ℹ️ How It Works", callback_data="info")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ===== COMMANDS =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.application.bot_data["chat_id"] = update.effective_chat.id

    await update.message.reply_text(
        "🤖 *PrimeX Signal Hub*\n\n"
        "🔴🔵🟣 Live signal feed active\n"
        "📊 Updates drop automatically\n\n"
        "👇 Use the menu below",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# ===== AUTO POST TASK =====
async def auto_updates(app):
    await asyncio.sleep(15)
    while True:
        chat_id = app.bot_data.get("chat_id")
        if chat_id:
            try:
                await app.bot.send_message(
                    chat_id=chat_id,
                    text=random.choice(UPDATE_MESSAGES),
                    parse_mode="Markdown",
                    reply_markup=main_menu()
                )
            except:
                pass
        await asyncio.sleep(60)  # every 1 minute

# ===== RUN =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.create_task(auto_updates(app))
    app.run_polling()

if __name__ == "__main__":
    main()
