import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# ---------------- CONFIG ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🆓 Free Signals", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Signals", callback_data="vip")],
        [InlineKeyboardButton("🎮 Games", callback_data="games")],
        [InlineKeyboardButton("💳 Subscribe", callback_data="subscribe")],
        [InlineKeyboardButton("ℹ️ About Bot", callback_data="about")]
    ]

    await update.message.reply_text(
        "👋 *Welcome to Primpex Drops Bot*\n\nChoose an option 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# ---------------- BUTTON HANDLER ----------------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    if q.data == "free":
        text = "🆓 *Free Signals*\n\n• Light predictions\n• Basic analysis"
    elif q.data == "vip":
        text = "🔒 *VIP Signals*\n\nSubscribe to unlock premium drops."
    elif q.data == "games":
        text = "🎮 *VIP Games*\n\n• Aviator ✈️\n• Virtual 🎰"
    elif q.data == "subscribe":
        text = "💳 *Subscription*\n\nPayment system coming soon."
    else:
        text = "ℹ️ *Primpex Drops Bot*\nPlay responsibly."

    await q.edit_message_text(text, parse_mode="Markdown")

# ---------------- MAIN ----------------
def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN not set")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("🤖 Bot running on Railway...")
    app.run_polling(
        poll_interval=3,
        timeout=30,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
