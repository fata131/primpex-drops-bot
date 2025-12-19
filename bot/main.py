import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# -------- START --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🆓 Free Signals", "💎 VIP Signals"],
        ["🎮 Games", "💳 Subscribe"],
        ["ℹ️ About Bot"]
    ]

    reply_keyboard = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        persistent=True
    )

    await update.message.reply_text(
        "👋 *Welcome to Primpex Drops Bot*\n\nSelect an option below 👇",
        reply_markup=reply_keyboard,
        parse_mode="Markdown"
    )

# -------- MENU HANDLER --------
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🆓 Free Signals":
        reply = "🆓 *Free Signals*\n\n• Basic drops\n• Light analysis"
    elif text == "💎 VIP Signals":
        reply = "🔒 *VIP Signals*\n\nSubscribe to unlock premium signals."
    elif text == "🎮 Games":
        reply = "🎮 *Games*\n\n• Aviator ✈️\n• Virtual 🎰"
    elif text == "💳 Subscribe":
        reply = "💳 *Subscription*\n\nPayment setup coming soon."
    elif text == "ℹ️ About Bot":
        reply = "ℹ️ *Primpex Drops Bot*\n\nPlay responsibly."
    else:
        reply = "❌ Use the menu buttons below."

    await update.message.reply_text(reply, parse_mode="Markdown")

# -------- MAIN --------
def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN not set")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))

    print("🤖 Bot running on Railway...")
    app.run_polling(
        poll_interval=3,
        timeout=30,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
