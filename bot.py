import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, User, ChatJoinRequest

my_bot=Client(
    "Bot Started",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

CHAT_ID=int(os.environ.get("CHAT_ID", None))
TEXT=os.environ.get("APPROVED_WELCOME_TEXT", "Hello {mention}\nWelcome To {title}\n\nYour Auto Approved")
APPROVED = os.environ.get("APPROVED_WELCOME", "on").lower()

@my_bot.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    approvedbot = await client.get_me() 
    button=[[
      InlineKeyboardButton("Update", url="https://t.me/MWUpdatez"),
      InlineKeyboardButton("Support", url="https://t.me/OpusTechz")
      ],[
      InlineKeyboardButton("Subscribe", url=f"https://youtube.com/channel/UCf_dVNrilcT0V2R--HbYpMA")
      ]]
    await message.reply_text(text="**Hello...⚡\n\nIam Telegram bot.\For the chat... \nVideo on my Channel**", reply_markup=InlineKeyboardMarkup(button), disable_web_page_preview=True)

@my_bot.on_chat_join_request(filters.chat(CHAT_ID))
async def autoapprove(client, message):
    chat=message.chat # Chat
    user=message.from_user # User
    print(f"{user.first_name} Joined ⚡") # Logs
    await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
    if APPROVED == "on":
        await client.send_message(chat_id=chat.id, text=TEXT.format(mention=user.mention, title=chat.title))       

print("Bottt..")
my_bot.run()
