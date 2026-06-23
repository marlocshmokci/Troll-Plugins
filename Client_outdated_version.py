# v0.1 — First attack
from telethon import TelegramClient, events

API_ID = 0
API_HASH = ""
MY_USER_ID = 0

client = TelegramClient("session", API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    if event.raw_text == ".op":  # .ор
        await event.reply("you are a fool")

client.start()
client.run_until_disconnected()
