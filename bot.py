import os
import logging
from pyrogram import Client, filters
from pyrogram.errors import BadMsgNotification
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create a logger
logger = logging.getLogger(__name__)

# Initialize the bot
my_bot = Client(
    "Bot Started",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)

CHAT_ID = int(os.environ.get("CHAT_ID", None))
TEXT = os.environ.get("APPROVED_WELCOME_TEXT", "Hello {mention}\nWelcome To {title}\n\nYour Auto Approved")
APPROVED = os.environ.get("APPROVED_WELCOME", "on").lower()

@my_bot.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    try:
        approvedbot = await client.get_me() 
        button=[
            [InlineKeyboardButton("Update", url="https://t.me/MWUpdatez"),
             InlineKeyboardButton("Support", url="https://t.me/OpusTechz")],
            [InlineKeyboardButton("Subscribe", url="https://youtube.com/channel/UCf_dVNrilcT0V2R--HbYpMA")]
        ]
        await message.reply_text(text="**Hello...⚡\n\nI am a Telegram bot. For the chat... \nVideo on my Channel**", reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview=True)
    except Exception as e:
        logger.exception("An error occurred in start command handler: %s", e)

@my_bot.on_chat_join_request(filters.chat(CHAT_ID))
async def autoapprove(client, message):
    try:
        chat = message.chat
        user = message.from_user
        logger.info("%s Joined ⚡", user.first_name) # Logs
        await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
        if APPROVED == "on":
            await client.send_message(chat_id=chat.id, text=TEXT.format(mention=user.mention, title=chat.title))
    except BadMsgNotification as e:
        logger.warning("BadMsgNotification error occurred: %s", e)
        # Handle the synchronization issue here
    except Exception as e:
        logger.exception("An error occurred in autoapprove handler: %s", e)

logger.info("Bot started...")
my_bot.run()
