import os
import random
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")

WHATSAPP_GROUP = "https://chat.whatsapp.com/JPA9XEkRReQ3fpzQ7Y4Ldt?mode=hqrt3"
WHATSAPP_CHANNEL = "https://whatsapp.com/channel/0029VbBfAibCxoAtQplkir3Z"

# ================= MENU =================
def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🆓 Free Signals", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Signals", callback_data="vip")],
        [InlineKeyboardButton("📢 Community", callback_data="community")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
    ])

# ================= SIGNAL CONTENT =================
UPDATE_MESSAGES = [
    "🔴🔵🟣 *LIVE OBSERVATION*\n\n"
    "📊 Short low runs detected\n"
    "🧠 Best move: *wait & observe*",

    "📈🟣 *PATTERN UPDATE*\n\n"
    "🔄 Repeated low multipliers\n"
    "💡 Spike usually comes after patience",

    "⚠️🔴 *RISK ALERT*\n\n"
    "📉 High volatility\n"
    "💣 Crashes below 2.0x spotted",

    "🧠🔵 *SMART TIP*\n\n"
    "✔️ Pre-set cashout\n"
    "❌ Avoid emotional entries",

    "📢🔵 *JOIN COMMUNITY*\n\n"
    f"👉 Group:\n{WHATSAPP_GROUP}\n\n"
    f"👉 Channel:\n{WHATSAPP_CHANNEL}",
]

# ================= COMMANDS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.application.bot_data["chat_id"] = update.effective_chat.id
    await update.message.reply_text(
        "🤖 *PrimeX Signal Hub*\n\n"
        "🔔 Live updates every 1 minute\n"
        "👇 Use menu below",
        parse_mode="Markdown",
        reply_markup=menu(),
    )

# ================= BUTTON HANDLER =================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "free":
        text = "🆓 *Free Signals*\n\nLive observations only."
    elif query.data == "vip":
        text = "💎 *VIP Signals*\n\nPremium access coming soon."
    elif query.data == "community":
        text = (
            "📢 *Join Community*\n\n"
            f"{WHATSAPP_GROUP}\n\n{WHATSAPP_CHANNEL}"
        )
    else:
        text = "ℹ️ *PrimeX*\n\nReal-time observation bot."

    await query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=menu(),
    )

# ================= AUTO SIGNAL =================
async def auto_signal(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.application.bot_data.get("chat_id")
    if chat_id:
        await context.bot.send_message(
            chat_id=chat_id,
            text=random.choice(UPDATE_MESSAGES),
            parse_mode="Markdown",
            reply_markup=menu(),
        )

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    # JobQueue works NOW
    app.job_queue.run_repeating(auto_signal, interval=60, first=20)

    print("🤖 PrimeX Bot Running")
    app.run_polling()

if __name__ == "__main__":
    main()
