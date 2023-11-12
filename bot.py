from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from WeatherAPI import get_weather
import json

with open('myTokens.json') as json_file:
    data = json.load(json_file)

# Extract token
token = data.get('token', None)

TELEGRAM_TOKEN : Final = data.get('telegramToken', None)
BOT_USERNAME : Final = "@SwedwishWeatherBot"

user_data = {}

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {
            "waitingForCity":False,
            "city":"",
            "lang":"en",
            "waitingForLang":False
            }
    await update.message.reply_text("Hello! Thanks for using this bot! I will help you figure out the weather in case you were banned from Google!")
    
async def get_weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if user_data[update.message.from_user.id]["city"] == "":
        await update.message.reply_text("Please, set city using 'set_city' command first.")
        return
    result = get_weather(city_name = user_data[update.message.from_user.id]["city"], lang=user_data[update.message.from_user.id]["lang"])
    if result == "":
        await update.message.reply_text("Wheather data not found. Try reentering city name.")
    else:
        await update.message.reply_text(result)
    
async def set_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.message.from_user.id]["waitingForCity"] = True
    await update.message.reply_text("Sure! Please input your city.")
    
async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.message.from_user.id]["waitingForLang"] = True
    await update.message.reply_text("Sure! Please input your language. ('en' for english, 'ru' for russian)")
    

#Responses

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    if user_data[update.message.from_user.id]["waitingForLang"]:
        user_data[update.message.from_user.id]["lang"] = text.strip()
        response = "New language set successfuly."
        user_data[update.message.from_user.id]["waitingForLang"] = False
        print("Bot:"+ response)
        await update.message.reply_text(response)
        return
    
    elif user_data[update.message.from_user.id]["waitingForCity"]:
        user_data[update.message.from_user.id]["city"] = text.strip()
        response = "New city set successfuly."
        print("Bot:"+ response)
        user_data[update.message.from_user.id]["waitingForCity"] = False
        await update.message.reply_text(response)
        return
    
    response = "I do not understand you. If you want to set city use 'set_city' command. If you want to set language use 'set_language' command."
    print("Bot:"+ response)
    await update.message.reply_text(response)
    
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} coused  error {context.error}")
    
if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Command
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("get_weather", get_weather_command))
    app.add_handler(CommandHandler("set_city", set_city))
    app.add_handler(CommandHandler("set_lang", set_lang))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Errors
    app.add_error_handler(error)
    
    # Polling
    print("Polling")
    app.run_polling(poll_interval=3)