import os
from dotenv import load_dotenv
from telegram import Bot

# Load .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")

# Check settings
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN .env me nahi mila")

if not OWNER_ID:
    raise ValueError("OWNER_ID .env me nahi mila")

OWNER_ID = int(OWNER_ID)

# Telegram bot
bot = Bot(BOT_TOKEN)


async def send_lead(
    source,
    text,
    score,
    category,
    link=""
):
    message = f"""
{category} LEAD

📊 Score: {score}/100
📢 Source: {source}

━━━━━━━━━━━━━━

{text[:2500]}

━━━━━━━━━━━━━━
"""

    if link:
        message += f"\n🔗 Original post:\n{link}"

    await bot.send_message(
        chat_id=OWNER_ID,
        text=message
    )
