import os
import asyncio
import random
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 6858086328
VIP_PRICE = "₦10,000"
VIP_DAYS = 30

BANK_DETAILS = (
    "🏦 *Bank Payment Details*\n\n"
    "Bank: *Opay*\n"
    "Account Number: *9163998203*\n"
    "Account Name: *Lukmon Fatai Olamide*\n\n"
    "Amount: *₦10,000*"
)

WHATSAPP_GROUP = "https://chat.whatsapp.com/JPA9XEkRReQ3fpzQ7Y4Ldt?mode=hqrt3"
WHATSAPP_CHANNEL = "https://whatsapp.com/channel/0029VbBfAibCxoAtQplkir3Z"

USERS = set()
VIP_USERS = {}

# ================= SIGNALS =================
FREE_SIGNALS = [
    "🔴🔵 *Market Watch*\nLow runs detected — observe patiently.",
    "🟣 *Risk Alert*\nHigh volatility — reduce stake.",
    "🔵 *Smart Tip*\nNever chase losses.",
    "🟣 *Behavior Notice*\nCalm players last longer.",
    "🔴 *Pattern Monitor*\nShort flights detected."
]

VIP_SIGNALS = [
    "💎 *VIP SIGNAL*\nBias: Medium spike likely\nConfidence: 78%",
    "💎 *VIP ALERT*\nFake dips detected — wait 1 round",
    "💎 *VIP INSIGHT*\nMomentum building — safer entry",
    "💎 *VIP ZONE*\nControlled entry advised"
]

# ================= HELPERS =================
def is_vip(user_id):
    return user_id in VIP_USERS and VIP_USERS[user_id] > datetime.datetime.utcnow()

def main_menu(user_id):
    buttons = [
        [InlineKeyboardButton("📊 Free Signals", callback_data="free")],
        [InlineKeyboardButton("💎 VIP Signals 🔒", callback_data="vip")],
        [InlineKeyboardButton("💳 Pay for VIP", callback_data="pay")],
        [InlineKeyboardButton("📈 My Status", callback_data="status")],
        [InlineKeyboardButton("📢 WhatsApp Group", url=WHATSAPP_GROUP)],
        [InlineKeyboardButton("📣 WhatsApp Channel", url=WHATSAPP_CHANNEL)],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
    ]

    if is_vip(user_id):
        buttons[1] = [InlineKeyboardButton("💎 VIP Signals", callback_data="vip")]

    return InlineKeyboardMarkup(buttons)

# ================= COMMANDS =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    USERS.add(user_id)

    await update.message.reply_text(
        "🤖 *PrimeX Signal Hub*\n\n"
        "🔔 Auto updates every 1 minute\n"
        "💎 VIP unlocks premium signals\n\n"
        "👇 Choose below",
        parse_mode="Markdown",
        reply_markup=main_menu(user_id)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    user_id = q.from_user.id

    if q.data == "free":
        await q.message.reply_text(random.choice(FREE_SIGNALS), parse_mode="Markdown")

    elif q.data == "vip":
        if not is_vip(user_id):
            await q.message.reply_text(
                "🔒 *VIP Locked*\n\nClick *Pay for VIP* to unlock.",
                parse_mode="Markdown"
            )
        else:
            await q.message.reply_text(random.choice(VIP_SIGNALS), parse_mode="Markdown")

    elif q.data == "pay":
        await q.message.reply_text(
            BANK_DETAILS,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ I Have Paid", callback_data="paid")]
            ])
        )

    elif q.data == "paid":
        await context.bot.send_message(
            ADMIN_ID,
            f"💰 *VIP PAYMENT REQUEST*\nUser ID: `{user_id}`",
            parse_mode="Markdown"
        )
        await q.message.reply_text("✅ Payment sent for approval.")

    elif q.data == "status":
        status = "💎 VIP" if is_vip(user_id) else "🆓 Free"
        await q.message.reply_text(f"📊 *Status:* {status}", parse_mode="Markdown")

    elif q.data == "help":
        await q.message.reply_text(
            "ℹ️ *Help*\n\n"
            "• Free signals auto-drop\n"
            "• VIP lasts 30 days\n"
            "• VIP unlock after payment approval",
            parse_mode="Markdown"
        )

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage: /approve USER_ID")
        return

    uid = int(context.args[0])
    VIP_USERS[uid] = datetime.datetime.utcnow() + datetime.timedelta(days=VIP_DAYS)

    await update.message.reply_text("✅ VIP Approved")
    await context.bot.send_message(uid, "🎉 *VIP Activated*", parse_mode="Markdown")

# ================= AUTO SIGNAL LOOP =================
async def auto_signal_loop(app):
    while True:
        for uid in list(USERS):
            try:
                await app.bot.send_message(
                    uid,
                    random.choice(FREE_SIGNALS),
                    parse_mode="Markdown"
                )
            except:
                pass
        await asyncio.sleep(60)

# ================= MAIN =================
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CallbackQueryHandler(buttons))

    await app.initialize()
    await app.start()

    asyncio.create_task(auto_signal_loop(app))

    await app.bot.initialize()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
