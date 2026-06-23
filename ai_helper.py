from telethon import TelegramClient, events
import asyncio
import g4f

# === INSERT YOUR DATA ===
API_ID = 0  # Your API_ID
API_HASH = ""  # Your API_HASH
MY_USER_ID = 0  # Your user ID

SESSION = "ai_helper_session"

# === SYSTEM PROMPT (AI instruction) ===
# Change the text inside quotes to customize the bot's personality
SYSTEM_PROMPT = """You are a friendly and witty conversationalist.
You reply briefly, to the point, with a bit of irony.
Always maintain a respectful tone.
Your task is to keep the conversation going, ask clarifying questions, and be pleasant to talk to."""

# === GREETING MESSAGE (sent on first message) ===
GREETING_MESSAGE = "Hello! I'm an AI assistant. How can I help you? 😊"

# === DIALOGUE HISTORY (per chat) ===
chat_histories = {}  # {chat_id: [list of messages]}
MAX_HISTORY = 10  # Number of last messages to remember

client = TelegramClient(SESSION, API_ID, API_HASH)

def get_ai_response(chat_id, user_message):
    # Get history for this chat
    history = chat_histories.get(chat_id, [])
    
    # Add user message to history
    history.append({"role": "user", "content": user_message})
    
    # Build request to AI
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + history[-MAX_HISTORY:]  # Take last N messages
    
    try:
        # Generate response via G4F (free, no keys required)
        response = g4f.ChatCompletion.create(
            model=g4f.models.default,
            messages=messages,
        )
        ai_reply = response
        
        # Save response to history
        history.append({"role": "assistant", "content": ai_reply})
        chat_histories[chat_id] = history
        
        return ai_reply
    except Exception as e:
        print(f"AI Error: {e}")
        return "Sorry, I'm a bit stuck. Try again."

@client.on(events.NewMessage)
async def ai_handler(event):
    # Check that it's a private message and not from us
    if not event.is_private:
        return
    if event.out:
        return
    
    chat_id = event.chat_id
    user_message = event.raw_text
    
    # Check if history exists for this chat
    if chat_id not in chat_histories:
        # First dialogue — send greeting
        await client.send_message(chat_id, GREETING_MESSAGE)
        chat_histories[chat_id] = []
    
    # Generate and send AI response
    ai_reply = get_ai_response(chat_id, user_message)
    await client.send_message(chat_id, ai_reply)

async def main():
    await client.start()
    print("🤖 AI Assistant started!")
    print("📩 Responds to all messages in DMs.")
    print("Press Ctrl+C to exit.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n❌ Exit...")
