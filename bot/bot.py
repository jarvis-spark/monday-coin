"""
$MONDAY Telegram Bot
Anonymous community manager for @MondayOnSol
"""

import os
import logging
import asyncio
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
from datetime import datetime, time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, CallbackQueryHandler
)
from telegram.constants import ParseMode

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ── CONFIG ────────────────────────────────────────────────────────────────────
BOT_TOKEN   = os.environ.get("MONDAY_BOT_TOKEN", "")
CA          = os.environ.get("MONDAY_CA", "TBA — follow @MondayOnSol")
CHART_URL   = os.environ.get("MONDAY_CHART_URL", "https://dexscreener.com")
BUY_URL     = os.environ.get("MONDAY_BUY_URL", "https://pump.fun")
WEBSITE_URL = os.environ.get("MONDAY_WEBSITE_URL", "https://mondayonsol.com")
TWITTER_URL = "https://x.com/MondayOnSol"

# ── COPY ──────────────────────────────────────────────────────────────────────
WELCOME_MSG = """
☕🟡 *Welcome to $MONDAY* 🟡☕

You made it. Against all odds — broken coffee machines, passive-aggressive emails, the 6am alarm — you found us.

*$MONDAY* is the Solana meme coin based on the world's most universally hated day. Every Monday morning, billions of people meme about this. We just put it on-chain.

📌 *Quick Links:*
• 🌐 [Website]({website})
• 🐦 [Twitter/X]({twitter})
• 📊 [Chart]({chart})
• 🪙 CA: `{ca}`
• 🛒 [Buy on pump.fun]({buy})

📋 *Rules (short, because it's Monday):*
1. No spam
2. No scam links — the only CA is pinned
3. Memes are mandatory
4. Be cool. It's already Monday.
5. Admins will NEVER DM you first. Block anyone who does.

You hate Mondays. You hold Mondays now. That's called growth. ☕
""".format(website=WEBSITE_URL, twitter=TWITTER_URL, chart=CHART_URL, ca=CA, buy=BUY_URL)

HELP_MSG = """
🤖 *$MONDAY Bot Commands*

/ca — Contract address
/buy — How to buy $MONDAY
/chart — Live chart
/links — All official links
/tokenomics — Token details
/roadmap — Where we're going
/monday — Monday motivation ☕
/help — This message

_Built by the $MONDAY team. You hate it. You need it._
"""

TOKENOMICS_MSG = """
🟡 *$MONDAY Tokenomics*

🪙 *Supply:* 1,000,000,000 (1 Billion)
💸 *Tax:* 0% — zero, none, nada
🔥 *LP:* Burned — no rug possible
⛓️ *Chain:* Solana
🚀 *Launch:* Fair launch on pump.fun
✅ *Mint Authority:* Revoked
✅ *Freeze Authority:* Revoked

No presale. No team allocation. No VC unlock. Just vibes and Monday energy. ☕
"""

ROADMAP_MSG = """
📅 *$MONDAY Roadmap*

*Phase 1 — "The Alarm Goes Off"*
✅ Token deployed
✅ LP burned, contract renounced
✅ Twitter & Telegram live
🎯 1,000 holders
🎯 CoinGecko & CMC listing

*Phase 2 — "The Second Alarm"*
🎯 10,000 holders
🎯 CEX listings
🎯 KOL partnerships
🎯 Meme contest

*Phase 3 — "Fine. We're Up."*
🎯 50,000 holders
🎯 Merch drop
🎯 Major CEX tier-2
🎯 Weekly Monday Report

*Phase 4 — "We Are The Monday"*
🎯 100,000+ holders
🎯 Tier-1 CEX listing
🎯 $MONDAY becomes the internet's Monday coin. Forever.

_Disclaimer: meme coin. We'll try our best. That's more than most Mondays deserve._
"""

MONDAY_QUOTES = [
    "Monday is just Friday in disguise. A very bad disguise. 😩",
    "The only good Monday is one where your $MONDAY portfolio is up. ☕",
    "You didn't choose Monday. Monday chose you. 🟡",
    "Every Monday is a new opportunity to hold $MONDAY and suffer with purpose.",
    "Monday called. We tokenized it. You're welcome.",
    "The alarm went off. The coffee's weak. The chart is green. It balances out. 📈",
    "Monday is the world's most reliable content creator. Every 7 days. Free. Forever.",
    "Some people hate Mondays. We profit from them. Different species.",
]

# ── COMMAND HANDLERS ──────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("🛒 Buy $MONDAY", url=BUY_URL),
         InlineKeyboardButton("📊 Chart", url=CHART_URL)],
        [InlineKeyboardButton("🌐 Website", url=WEBSITE_URL),
         InlineKeyboardButton("🐦 Twitter", url=TWITTER_URL)],
    ]
    await update.message.reply_text(
        WELCOME_MSG,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def ca_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🪙 *$MONDAY Contract Address*\n\n`{CA}`\n\n"
        f"Always verify on [DexScreener]({CHART_URL}) before buying. "
        f"The only real CA is pinned in this group.",
        parse_mode=ParseMode.MARKDOWN
    )

async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🛒 *How to Buy $MONDAY*\n\n"
        "1️⃣ Get [Phantom Wallet](https://phantom.app) — best Solana wallet\n"
        "2️⃣ Buy SOL on any exchange (Coinbase, Binance, Kraken)\n"
        "3️⃣ Send SOL to your Phantom wallet\n"
        f"4️⃣ Go to [pump.fun]({BUY_URL}) or [Raydium](https://raydium.io)\n"
        f"5️⃣ Paste CA: `{CA}`\n"
        "6️⃣ Swap SOL for $MONDAY ☕\n\n"
        "_Set slippage to 1–3% if the swap fails._"
    )
    kb = [[InlineKeyboardButton("🛒 Buy Now", url=BUY_URL)]]
    await update.message.reply_text(
        msg, parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def chart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("📊 Live Chart", url=CHART_URL)]]
    await update.message.reply_text(
        "📊 *$MONDAY Live Chart*\n\nClick below for real-time price and volume.",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def links_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🔗 *Official $MONDAY Links*\n\n"
        f"🌐 Website: {WEBSITE_URL}\n"
        f"🐦 Twitter: {TWITTER_URL}\n"
        f"📊 Chart: {CHART_URL}\n"
        f"🛒 Buy: {BUY_URL}\n"
        f"🪙 CA: `{CA}`\n\n"
        f"_If a link looks different, it's a scam. These are the only official links._",
        parse_mode=ParseMode.MARKDOWN
    )

async def tokenomics_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TOKENOMICS_MSG, parse_mode=ParseMode.MARKDOWN)

async def roadmap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ROADMAP_MSG, parse_mode=ParseMode.MARKDOWN)

async def monday_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random
    quote = random.choice(MONDAY_QUOTES)
    await update.message.reply_text(f"☕ _{quote}_", parse_mode=ParseMode.MARKDOWN)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_MSG, parse_mode=ParseMode.MARKDOWN)

# ── NEW MEMBER WELCOME ────────────────────────────────────────────────────────
async def welcome_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.is_bot:
            continue
        name = member.first_name or "fren"
        kb = [
            [InlineKeyboardButton("🛒 Buy $MONDAY", url=BUY_URL),
             InlineKeyboardButton("📊 Chart", url=CHART_URL)],
        ]
        await update.message.reply_text(
            f"☕ Welcome, *{name}*! You've found $MONDAY — the coin you never knew you needed.\n\n"
            f"Check /help for commands. CA is pinned. Admins never DM first.\n\n"
            f"_You hate it. You need it._ 🟡",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(kb)
        )

# ── ANTI-SPAM ─────────────────────────────────────────────────────────────────
BANNED_KEYWORDS = ["airdrop", "giveaway dm", "send sol", "double your", "investment opportunity"]

async def spam_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    text = update.message.text.lower()
    for kw in BANNED_KEYWORDS:
        if kw in text:
            try:
                await update.message.delete()
                await context.bot.ban_chat_member(
                    update.effective_chat.id,
                    update.effective_user.id
                )
                logger.info(f"Banned {update.effective_user.id} for spam keyword: {kw}")
            except Exception as e:
                logger.error(f"Failed to ban/delete: {e}")
            return

# ── MONDAY MORNING SCHEDULER ──────────────────────────────────────────────────
async def monday_morning_post(context: ContextTypes.DEFAULT_TYPE):
    """Posted every Monday morning at 08:00 UTC"""
    chat_id = context.job.chat_id
    now = datetime.utcnow()
    if now.weekday() != 0:  # 0 = Monday
        return
    
    import random
    quote = random.choice(MONDAY_QUOTES)
    
    msg = (
        f"☕ *Good morning. It's Monday.*\n\n"
        f"_{quote}_\n\n"
        f"🟡 *$MONDAY* — the only coin that gets stronger every Monday.\n\n"
        f"📊 Chart: {CHART_URL}\n"
        f"🛒 Buy: {BUY_URL}"
    )
    try:
        await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error(f"Monday morning post failed: {e}")

# ── MAIN ──────────────────────────────────────────────────────────────────────
async def main():
    if not BOT_TOKEN:
        raise ValueError("MONDAY_BOT_TOKEN environment variable not set")

    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start",       start))
    app.add_handler(CommandHandler("ca",          ca_command))
    app.add_handler(CommandHandler("buy",         buy_command))
    app.add_handler(CommandHandler("chart",       chart_command))
    app.add_handler(CommandHandler("links",       links_command))
    app.add_handler(CommandHandler("tokenomics",  tokenomics_command))
    app.add_handler(CommandHandler("roadmap",     roadmap_command))
    app.add_handler(CommandHandler("monday",      monday_command))
    app.add_handler(CommandHandler("help",        help_command))

    # Welcome new members
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_members))

    # Anti-spam (group messages only)
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, spam_filter))

    logger.info("$MONDAY bot starting...")
    async with app:
        await app.start()
        await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        logger.info("Bot is running. Press Ctrl+C to stop.")
        await asyncio.Event().wait()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
