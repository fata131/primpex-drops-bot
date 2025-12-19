import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ================== CONFIG ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")

WHATSAPP_GROUP = "https://chat.whatsapp.com/JPA9XEkRReQ3fpzQ7Y4Ldt?mode=hqrt3"
WHATSAPP_CHANNEL = "https://whatsapp.com/channel/0029VbBfAibCxoAtQplkir3Z"

# ================== MENU ==================
def menu():
    keyboard = [
        [InlineKeyboardButton("🆓 Free Signals", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Signals", callback_data="vip")],
        [InlineKeyboardButton("🎮 Games", callback_data="games")],
        [InlineKeyboardButton("📢 Community", callback_data="community")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ================== LIVE UPDATES ==================
UPDATE_MESSAGES = [
    "🔴🔵🟣 *LIVE GAME OBSERVATION*\n\n"
    "📊 Aviator showing *short low runs*\n"
    "🧠 Best action: *observe first*\n\n"
    "⚠️ Rushing causes losses",

    "📈🟣 *PATTERN MONITOR*\n\n"
    "🔄 Repeated low multipliers detected\n"
    "💡 Medium spike often comes *after patience*",

    "⚠️🔴 *RISK ALERT*\n\n"
    "📉 High volatility detected\n"
    "💣 Multiple crashes below 2.0x",

    "🧠🔵 *SMART PLAY TIP*\n\n"
    "✔️ Always pre-set cashout\n"
    "❌ Avoid emotional entry",

    "📊🟣 *PLAYER BEHAVIOR INSIGHT*\n\n"
    "👥 80% lose by chasing losses\n"
    "🧠 Calm players last longer",

    "📢🔵 *COMMUNITY UPDATE*\n\n"
    f"👉 WhatsApp Group:\n{WHATSAPP_GROUP}\n\n"
    f"👉 WhatsApp Channel:\n{WHATSAPP_CHANNEL}\n\n"
    "🚀 Stay connected",
]

# ================== COMMANDS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    context.application.bot_data["chat_id"] = chat_id

    await update.message.reply_text(
        "🤖 *PrimeX Signal Hub*\n\n"
        "🔴🔵🟣 Live updates ACTIVE\n"
        "⏱ Signals drop every 1 minute\n\n"
        "👇 Use the menu below",
        parse_mode="Markdown",
        reply_markup=menu(),
    )

# ================== BUTTON HANDLER ==================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "free":
        text = "🆓 *Free Signals*\n\nLive observations & safety tips.\nUpgrade to VIP for deeper analysis."
    elif query.data == "vip":
        text = "💎 *VIP Signals*\n\nPremium entries coming soon.\nSubscription required."
    elif query.data == "games":
        text = "🎮 *Games Supported*\n\n✈️ Aviator\n🎰 Virtual Games\n🍾 Bottle Spin"
    elif query.data == "community":
        text = (
            "📢 *Join Our Community*\n\n"
            f"👉 Group:\n{WHATSAPP_GROUP}\n\n"
            f"👉 Channel:\n{WHATSAPP_CHANNEL}"
        )
    else:
        text = (
            "ℹ️ *About PrimeX*\n\n"
            "We provide real-time observations\n"
            "to help reduce blind losses."
        )

    await query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=menu(),
    )

# ================== AUTO SIGNAL JOB ==================
async def auto_signal(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.application.bot_data.get("chat_id")
    if not chat_id:
        return

    await context.bot.send_message(
        chat_id=chat_id,
        text=random.choice(UPDATE_MESSAGES),
        parse_mode="Markdown",
        reply_markup=menu(),
    )

# ================== MAIN ==================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    # Run auto signal every 60 seconds
    app.job_queue.run_repeating(auto_signal, interval=60, first=15)

    print("🤖 PrimeX Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
