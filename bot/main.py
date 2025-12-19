import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ===== ENV =====
BOT_TOKEN = os.getenv("BOT_TOKEN")

WHATSAPP_GROUP = "https://chat.whatsapp.com/JPA9XEkRReQ3fpzQ7Y4Ldt?mode=hqrt3"
WHATSAPP_CHANNEL = "https://whatsapp.com/channel/0029VbBfAibCxoAtQplkir3Z"

# ===== SIGNAL CONTENT =====
UPDATE_MESSAGES = [
    "🔴🔵🟣 *LIVE GAME OBSERVATION*\n\n"
    "📊 Fast low runs detected\n"
    "🧠 Best move: *observe*\n\n"
    "⚠️ Blind entry = loss",

    "📈🟣 *PATTERN MONITOR*\n\n"
    "🔄 Short flights ongoing\n"
    "💡 Spike comes after patience\n\n"
    "✅ Stay calm",

    "⚠️🔴 *RISK UPDATE*\n\n"
    "📉 High volatility\n"
    "💣 Crashes below 2.0x\n\n"
    "🧠 Reduce stake",

    "🧠🔵 *SMART TIP*\n\n"
    "✔️ Cashout early\n"
    "❌ No emotions\n\n"
    "📌 Discipline wins",

    "📢🔵 *COMMUNITY UPDATE*\n\n"
    f"👉 Group: {WHATSAPP_GROUP}\n"
    f"👉 Channel: {WHATSAPP_CHANNEL}\n\n"
    "🚀 Stay connected"
]

# ===== MENU =====
def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Live Signals", callback_data="signals")],
        [InlineKeyboardButton("💬 WhatsApp Group", url=WHATSAPP_GROUP)],
        [InlineKeyboardButton("📢 WhatsApp Channel", url=WHATSAPP_CHANNEL)],
    ])

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.application.bot_data["chat_id"] = update.effective_chat.id

    await update.message.reply_text(
        "🤖 *PrimeX Signal Hub*\n\n"
        "🔴🔵🟣 Live updates enabled\n"
        "⏱ Signals drop every minute\n\n"
        "👇 Use menu below",
        reply_markup=menu(),
        parse_mode="Markdown"
    )

# ===== AUTO SIGNAL JOB =====
async def auto_signal(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.application.bot_data.get("chat_id")
    if chat_id:
        await context.bot.send_message(
            chat_id=chat_id,
            text=random.choice(UPDATE_MESSAGES),
            parse_mode="Markdown",
            reply_markup=menu()
        )

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # JobQueue (SAFE & STABLE)
    app.job_queue.run_repeating(
        auto_signal,
        interval=60,   # every 1 minute
        first=15
    )

    app.run_polling()

if __name__ == "__main__":
    main()
