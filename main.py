import logging
import random
import requests
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
# Aapka Naya Token Update Kar Diya Gaya Hai
BOT_TOKEN = "6282042538:AAF3S69oNm-_qMbGUE8IqZFMnEp1sRpZd2c"
CHANNEL_URL = "https://t.me/+lN2xb-LBYPtjZTk1"
CREATOR_URL = "https://t.me/XCLUSIVEJEXAR"
WEBSITE_URL = "https://godjexaremotes.online"

# Region Specific APIs
REGION_URLS = {
    "ind": "https://anixh-emote-ind.vercel.app/play_emote",
    "bd": "https://anixh-emote-bd.vercel.app/play_emote",
    "id": "https://anixh-emote-id.vercel.app/play_emote",
    "pk": "https://anixh-emote-pk.vercel.app/play_emote"
}

# Emote IDs Database
EMOTE_IDS = {
    "909049010": "EVO P90",
    "909051003": "EVO M60 (NEW)", 
    "909033002": "EVO MP5",
    "909041005": "EVO GROZA",
    "909038010": "EVO THOMPSON",
    "909039011": "EVO M10 (RED)",
    "909040010": "EVO MP40 (BLUE)",
    "909000081": "EVO M10 (GREEN)",
    "909000085": "EVO XM8",
    "909000063": "EVO AK",
    "909000075": "EVO MP40",
    "909033001": "EVO M4A1",
    "909000090": "EVO FAMAS",
    "909000068": "EVO SCAR",
    "909000098": "EVO UMP",
    "909035007": "EVO M18",
    "909037011": "EVO FIST",
    "909038012": "EVO G18",
    "909035012": "EVO AN94",
    "909042008": "EVO WOODPECKER"
}

async def make_api_request(url, params):
    loop = asyncio.get_running_loop()
    try:
        return await loop.run_in_executor(None, lambda: requests.get(url, params=params, timeout=10))
    except Exception as e:
        raise e

async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    welcome_text = f"🎮 Welcome {user.first_name} to EVO Emote Bot! 🎮\n\nUse /help to see commands."
    keyboard = [[InlineKeyboardButton("📢 Join Channel", url=CHANNEL_URL)],
                [InlineKeyboardButton("👨‍💻 Creator", url=CREATOR_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def play(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 4:
        await update.message.reply_text("❌ Usage: /play region teamcode uid emote_id\nExample: /play ind 12345 67890 909049010")
        return
    
    region, team_code, uid, emote_id = context.args
    region = region.lower()
    
    if region not in REGION_URLS:
        await update.message.reply_text("❌ Invalid Region! Use ind, bd, id, or pk.")
        return

    api_url = REGION_URLS[region]
    processing_msg = await update.message.reply_text(f"🔄 Activating emote on {region.upper()}...")

    try:
        params = {'region': region, 'teamcode': team_code, 'uid': uid, 'uid2': '987654321', 'emote': emote_id}
        response = await make_api_request(api_url, params)
        data = response.json()
        
        if data.get('status') == 'error':
            await processing_msg.edit_text(f"❌ Error: {data.get('message')}")
        else:
            await processing_msg.edit_text(f"✅ Emote Activated!\n\nID: {emote_id}\nUID: {uid}")
    except Exception as e:
        await processing_msg.edit_text(f"🚨 Connection Error: {str(e)}")

async def get_emotes(update: Update, context: CallbackContext) -> None:
    emote_list = "🎮 EVO Emote IDs:\n\n"
    for eid, name in EMOTE_IDS.items():
        emote_list += f"`{eid}` - {name}\n"
    await update.message.reply_text(emote_list, parse_mode="Markdown")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", play))
    application.add_handler(CommandHandler("get", get_emotes))
    
    print("🤖 Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
