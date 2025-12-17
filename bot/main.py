import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ---------- START COMMAND ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🆓 Free Signals", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Signals", callback_data="vip")],
        [InlineKeyboardButton("🎮 Games", callback_data="games")],
        [InlineKeyboardButton("💳 Subscribe", callback_data="subscribe")],
        [InlineKeyboardButton("ℹ️ About Bot", callback_data="about")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Welcome to *Primpex Drops Bot*\n\n"
        "Choose an option below 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ---------- BUTTON HANDLER ----------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "free":
        await query.edit_message_text(
            "🆓 *Free Signals*\n\n"
            "• Light predictions\n"
            "• Basic analysis\n"
            "• No guarantees\n\n"
            "Upgrade to VIP for stronger drops 🔒",
            parse_mode="Markdown"
        )

    elif query.data == "vip":
        await query.edit_message_text(
            "🔒 *VIP Signals*\n\n"
            "This feature is locked.\n"
            "Subscribe to access premium predictions.",
            parse_mode="Markdown"
        )

    elif query.data == "games":
        await query.edit_message_text(
            "🎮 *Available Games (VIP)*\n\n"
            "• Aviator ✈️\n"
            "• Virtual Games 🎰\n"
            "• Bottle Spin 🍾\n\n"
            "🔒 VIP members only.",
            parse_mode="Markdown"
        )

    elif query.data == "subscribe":
        await query.edit_message_text(
            "💳 *Subscription*\n\n"
            "VIP access coming soon.\n"
            "Payment system will be added next step.",
            parse_mode="Markdown"
        )

    elif query.data == "about":
        await query.edit_message_text(
            "ℹ️ *About This Bot*\n\n"
            "Primpex Drops Bot helps users\n"
            "reduce losses and improve timing.\n\n"
            "⚠️ Play responsibly.",
            parse_mode="Markdown"
        )

# ---------- MAIN ----------
def main():
    print("🤖 Bot starting...")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot running...")
    app.run_polling(
        poll_interval=2,
        timeout=20,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
