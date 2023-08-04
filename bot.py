# Import the necessary libraries
from googletrans import Translator, LANGUAGES
from telebot.async_telebot import AsyncTeleBot
import asyncio
from telebot.types import ReplyKeyboardMarkup
from telebot import types

# Import the bot token from the config.py file
from config import BOT_TOKEN

# Create the bot instance
bot = AsyncTeleBot(BOT_TOKEN, parse_mode=None)

# Dictionaries to store the first and second translation languages for each user
user_translation_language = {}
user_second_translation_language = {}

# Function to create the reply keyboard with the "Admin" and "Help" buttons in one row
def create_start_reply_keyboard():
    reply_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    reply_keyboard.add('/admin', '/help')
    return reply_keyboard

# Handler for the /start command
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message, 'Hello, ' + message.from_user.first_name + '.\n'
                                'I will translate from Russian to English and from other languages to Russian.',
                       reply_markup=create_start_reply_keyboard())

# Handler for the /admin command
@bot.message_handler(commands=['admin'])
async def admin_command(message):
    await bot.reply_to(message, 'test1', reply_markup=create_start_reply_keyboard())

# Function to get the list of available commands for /help
def get_available_commands():
    commands_list = [
        '/start - Start the bot',
        '/setlang - Set the first translation language',
        '/secondlang - Set the second translation language',
        '/status - Show the selected languages for translation',
        '/help - Show available commands'
    ]
    return "\n".join(commands_list)

# Handler for the /help command
@bot.message_handler(commands=['help'])
async def send_help(message):
    help_text = 'Available commands for the bot:\n' + get_available_commands()
    await bot.reply_to(message, help_text, reply_markup=create_start_reply_keyboard())

# Handler for the /setlang command
@bot.message_handler(commands=['setlang'])
async def set_language(message):
    try:
        lang_code = message.text.split(' ', 1)[1].lower()
        # Check if the chosen language exists
        if lang_code in LANGUAGES:
            user_translation_language[message.chat.id] = lang_code
            await bot.reply_to(message, 'First translation language set to: ' + LANGUAGES[lang_code])
        else:
            await bot.reply_to(message, 'Invalid language. Using English as the default language.')
    except IndexError:
        await bot.reply_to(message, 'Usage: /setlang language_code')

# Handler for the /secondlang command
@bot.message_handler(commands=['secondlang'])
async def set_second_language(message):
    try:
        lang_code = message.text.split(' ', 1)[1].lower()
        # Check if the chosen language exists
        if lang_code in LANGUAGES:
            user_second_translation_language[message.chat.id] = lang_code
            await bot.reply_to(message, 'Second translation language set to: ' + LANGUAGES[lang_code])
        else:
            await bot.reply_to(message, 'Invalid language. Using English as the default language.')
    except IndexError:
        await bot.reply_to(message, 'Usage: /secondlang language_code')

# Handler for the /status command
@bot.message_handler(commands=['status'])
async def show_status(message):
    first_lang = user_translation_language.get(message.chat.id, 'en')
    second_lang = user_second_translation_language.get(message.chat.id, 'ru')
    await bot.reply_to(message, 'First translation language: ' + LANGUAGES.get(first_lang, 'English') + '\n'
                                 'Second translation language: ' + LANGUAGES.get(second_lang, 'English'))

# Handler for text messages
@bot.message_handler()
async def user_text(message):
    translator = Translator()

    # Determine the input language or use the selected translation languages
    translation_lang = user_translation_language.get(message.chat.id, 'en')
    second_translation_lang = user_second_translation_language.get(message.chat.id, 'en')

    # Determine the input language of the message
    message_lang = translator.detect(message.text).lang

    # Translate the text to the corresponding language
    if message_lang == translation_lang:
        send = translator.translate(message.text, dest=second_translation_lang)
    else:
        send = translator.translate(message.text, dest=translation_lang)

    await bot.reply_to(message, send.text)

# Handler for pictures with captions
@bot.message_handler(content_types=['photo'])
async def handle_image(message):
    translator = Translator()
    # Handler for messages with images
    chat_id = message.chat.id
    photo = message.photo[-1].file_id
    caption = message.caption

    # Define the caption language or use the selected translation language
    translation_lang = user_translation_language.get(message.chat.id, 'en')

    # Translate the caption into the selected target language
    send = translator.translate(caption, dest=translation_lang)
    await bot.send_photo(chat_id, photo, caption=send.text)

# Inline request handler
@bot.inline_handler(lambda query: True)
async def inline_query(query):
    results = []
    translator = Translator()
    text = query.query.strip()

    # If the query is empty, don't translate
    if not text:
        return

    # Define the input language or use the selected translation language
    translation_lang = user_translation_language.get(query.from_user.id, 'en')

    # Translate the text into the selected target language
    send = translator.translate(text, dest=translation_lang)
    results.append(types.InlineQueryResultArticle(
        id='1', title=send.text, input_message_content=types.InputTextMessageContent(
            message_text=send.text)))

    await bot.answer_inline_query(query.id, results)

# Run and re-run on failure.
asyncio.run(bot.infinity_polling())

