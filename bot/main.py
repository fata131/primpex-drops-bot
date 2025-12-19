import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🔵 FREE SIGNALS 🔵", "🟣 VIP SIGNALS 🟣"],
        ["🔴 GAMES 🔴", "💳 SUBSCRIBE 💳"],
        ["ℹ️ ABOUT BOT"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Select an option ⬇️"
    )

    await update.message.reply_text(
        "🔥 *PRIMPEX DROPS BOT* 🔥\n\n"
        "🎯 *Smart signals*\n"
        "📊 *Clean analysis*\n"
        "💰 *Risk management*\n\n"
        "👇 Choose from menu below",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ===== MENU HANDLER =====
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "FREE" in text:
        msg = (
            "🔵 *FREE SIGNALS* 🔵\n\n"
            "✔ Light predictions\n"
            "✔ Market timing\n"
            "❌ No guarantee"
        )

    elif "VIP" in text:
        msg = (
            "🟣 *VIP SIGNALS* 🟣\n\n"
            "🔒 Locked content\n"
            "💎 High accuracy drops\n"
            "💳 Subscription required"
        )

    elif "GAMES" in text:
        msg = (
            "🔴 *AVAILABLE GAMES* 🔴\n\n"
            "✈️ Aviator\n"
            "🎰 Virtual Games\n"
            "🎲 More coming soon"
        )

    elif "SUBSCRIBE" in text:
        msg = (
            "💳 *SUBSCRIPTION* 💳\n\n"
            "📌 Weekly & Monthly plans\n"
            "📌 Payment setup coming next"
        )

    elif "ABOUT" in text:
        msg = (
            "ℹ️ *ABOUT PRIMPEX DROPS BOT*\n\n"
            "⚠️ Signals are guides only\n"
            "🎯 Discipline is key"
        )

    else:
        msg = "❌ Use the menu buttons below 👇"

    await update.message.reply_text(msg, parse_mode="Markdown")

# ===== MAIN =====
def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))

    print("🤖 Bot is live...")
    app.run_polling(timeout=30)

if __name__ == "__main__":
    main()
