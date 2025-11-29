# bot.py
import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from brain import get_ai_response
from knowledge_base import SALES_SCRIPTS

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # We could reset memory here if we wanted, but let's keep it persistent as requested.
    
    welcome_text = SALES_SCRIPTS["intro"]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text
    
    # Show "typing" status
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Get AI response
    # Run in executor to avoid blocking asyncio loop with sync OpenAI call
    loop = asyncio.get_running_loop()
    username = update.effective_user.username
    response = await loop.run_in_executor(None, get_ai_response, user_id, user_text, username)
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("Error: TELEGRAM_TOKEN not found in .env")
        exit(1)
        
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    print("Bot is running...")
    application.run_polling()
