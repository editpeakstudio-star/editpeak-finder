import os
import asyncio
import base64

from dotenv import load_dotenv
from telethon import TelegramClient, events

from config import MIN_SCORE
from database import init_db, save_lead
from lead_analyzer import analyze
from notifier import send_lead


load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")


SESSION_FILE = "editpeak_session.session"
SESSION_B64 = os.getenv("TELEGRAM_SESSION_B64")

if SESSION_B64 and not os.path.exists(SESSION_FILE):
    with open(SESSION_FILE, "wb") as f:
        f.write(base64.b64decode(SESSION_B64.strip()))

if not os.path.exists(SESSION_FILE):
    raise RuntimeError("Telegram session file is missing")

# Yahan baad me accessible Telegram sources add karenge.
SOURCES = [
    "Editpeakstudio",
    "Freelancing_Video_Editing",
    "redgs",
    "editing_material7",
    "@letsgrow10",
    "@NOXXCUT",
    "@techjailbreakofficial",
]

client = TelegramClient(
    "editpeak_session",
    API_ID,
    API_HASH
)


@client.on(events.NewMessage(chats=SOURCES))
async def handle_message(event):

    text = event.raw_text

    if not text:
        return

    chat = await event.get_chat()

    sender = await event.get_sender()

    username = "Unknown"

    if sender:
        if getattr(sender, "username", None):
            username = "@" + sender.username
        elif getattr(sender, "first_name", None):
            username = sender.first_name

    source = "Telegram"

    if getattr(chat, "username", None):
        source = "@" + chat.username
    elif getattr(chat, "title", None):
        source = chat.title

    print()
    print("╔══════════════════════════════════════╗")
    print(f"📩 SOURCE   : {source}")
    print(f"👤 USERNAME : {username}")
    print(f"🆔 MESSAGE  : {event.message.id}")
    print(f"📝 TEXT     : {text[:120]}")

    score, category = analyze(text)

    print(f"{category} SCORE: {score}/100")
    print("╚══════════════════════════════════════╝")
    print()
    print("────────────────────────────────────────")

    if score < MIN_SCORE:
        return

    source = "Telegram"

    try:
        chat = await event.get_chat()

        if getattr(chat, "username", None):
            source = "@" + chat.username
        elif getattr(chat, "title", None):
            source = chat.title

    except Exception:
        pass

    saved = save_lead(
        source,
        event.message.id,
        text,
        score,
        category
    )

    if not saved:
        return

    link = ""

    try:
        chat = await event.get_chat()

        if getattr(chat, "username", None):
            link = (
                f"https://t.me/"
                f"{chat.username}/"
                f"{event.message.id}"
            )

    except Exception:
        pass

    await send_lead(
        source,
        text,
        score,
        category,
        link
    )


async def main():

    init_db()

    print("""
=================================
       EDITPEAK STUDIO
       CLIENT FINDER
=================================

Starting...
""")

    await client.start()

    print("✅ Client Finder is running.")

    await client.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        import traceback
        print("❌ STARTUP ERROR:")
        traceback.print_exc()
        raise
