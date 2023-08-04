# Import the necessary libraries
import telebot
from googletrans import Translator, LANGUAGES
from telebot.async_telebot import AsyncTeleBot
import asyncio
from telebot.types import ReplyKeyboardMarkup
from telebot import types

import languages
import user_list
# Import the bot token from the config.py file
from config import BOT_TOKEN

# Create the bot instance
bot = AsyncTeleBot(BOT_TOKEN, parse_mode=None)
# Global variable to keep track of the user's language selection
flag = "1"

# Dictionaries to store the first and second translation languages for each user
user_translation_language = {}
user_second_translation_language = {}


# Function to create the reply keyboard with the "Support" and "Help" buttons in one row
def create_start_reply_keyboard():
    reply_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    reply_keyboard.add('❕Info', '📖Help')
    reply_keyboard.add('❤Support', '🌐Chosen Language')
    return reply_keyboard


# Function to get the list of available languages in Google Translate
def get_available_languages():
    sorted_languages = sorted(LANGUAGES.items(), key=lambda x: x[1])
    language_list = [f'{code} - {name}' for code, name in sorted_languages]
    return '\n'.join(language_list)


# Handler for the /languages command
@bot.message_handler(commands=['languages'])
async def show_languages(message):
    languages_list = get_available_languages()
    await bot.send_message(message.chat.id, 'Available languages for translation:\n' + languages_list,
                           reply_markup=create_start_reply_keyboard())


# Function to translate the message based on user's selected languages
def translate_message(message_text, from_lang, to_lang):
    translator = Translator()
    translation = translator.translate(message_text, src=from_lang, dest=to_lang)
    return translation.text


# Handler for the /start command
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    write_user_id(message.from_user.id)
    chat_id = message.chat.id
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(telebot.types.KeyboardButton("🇺🇸English"), telebot.types.KeyboardButton("🇷🇺Russian"))
    await bot.send_sticker(chat_id, 'CAACAgIAAxkBAAHY6rRkzT06HjGgmmR0FlRlU9tqb-RKJgACugADMNSdEYTXxIjEUGdWLwQ')
    await bot.send_message(chat_id, '👋Hello, ' + message.from_user.first_name + "!\n\n" +
                           "Select the language of the bot interface. The language can be changed later\n" +
                           "---------\n" +
                           "Выберите язык интерфейса бота. Язык можно изменить позднее", reply_markup=keyboard)


# Function to read original user id's from the file
def read_user_ids():
    try:
        with open('users.txt', 'r') as file:
            user_ids = file.readlines()
            return [int(uid.strip()) for uid in user_ids]
    except FileNotFoundError:
        return []


def write_user_id(user_id):
    with open('users.txt', 'a') as file:
        file.write(str(user_id) + '\n')


# Handler for the /root command
@bot.message_handler(commands=['root'])
async def root_command(message):
    await bot.send_message(message.chat.id, user_list.user_scanning(message))

# Handler for the /userreset command
@bot.message_handler(commands=['userreset'])
async def user_reset(message):
    await bot.send_message(message.chat.id, user_list.remove_duplicates_inplace(message, 'users.txt'))



@bot.message_handler(func=lambda message: message.text == "🇺🇸English")
async def handle_button_one(message):
    global flag
    flag = "0"
    await bot.send_message(message.chat.id, languages.get_start_info(flag), reply_markup=create_start_reply_keyboard())


@bot.message_handler(func=lambda message: message.text == "🇷🇺Russian")
async def handle_button_two(message):
    global flag
    flag = "1"
    await bot.send_message(message.chat.id, languages.get_start_info(flag), reply_markup=create_start_reply_keyboard())


# Handler for the ❤Support command
@bot.message_handler(commands=['support'])
@bot.message_handler(func=lambda message: message.text == '❤Support')
async def admin_command(message):
    print(user_second_translation_language)
    await bot.send_message(message.chat.id, 'Support - @marisweeti', reply_markup=create_start_reply_keyboard())


# Handler for the 📖Help command
@bot.message_handler(commands=['info'])
@bot.message_handler(func=lambda message: message.text == '📖Help')
async def admin_command(message):
    await bot.send_message(message.chat.id, languages.get_start_info(flag), reply_markup=create_start_reply_keyboard())


# Handler for the ❕Info command
@bot.message_handler(commands=['info'])
@bot.message_handler(func=lambda message: message.text == '❕Info')
async def send_help(message):
    help_text = languages.get_available_commands(flag)
    await bot.send_message(message.chat.id, help_text, reply_markup=create_start_reply_keyboard())


# Handler for the /first command
@bot.message_handler(commands=['first'])
async def set_language(message):
    try:
        lang_code = message.text.split(' ', 1)[1].lower()
        # Check if the chosen language exists
        if lang_code in LANGUAGES:
            user_translation_language[message.chat.id] = lang_code
            await bot.send_message(message.chat.id, 'First translation language set to: ' + LANGUAGES[lang_code])
        else:
            await bot.send_message(message.chat.id, 'Invalid language. Using English as the default language.')
    except IndexError:
        await bot.send_message(message.chat.id, 'Usage: /first language_code')


# Handler for the /second command
@bot.message_handler(commands=['second'])
async def set_second_language(message):
    try:
        lang_code = message.text.split(' ', 1)[1].lower()
        # Check if the chosen language exists
        if lang_code in LANGUAGES:
            user_second_translation_language[message.chat.id] = lang_code
            await bot.send_message(message.chat.id, 'Second translation language set to: ' + LANGUAGES[lang_code])
        else:
            await bot.send_message(message.chat.id, 'Invalid language. Using English as the default language.')
    except IndexError:
        await bot.send_message(message.chat.id, 'Usage: /second language_code')


# Handler for the /status command
@bot.message_handler(commands=['status'])
@bot.message_handler(func=lambda message: message.text == '🌐Chosen Language')
async def show_status(message):
    first_lang = user_translation_language.get(message.chat.id, 'en')
    second_lang = user_second_translation_language.get(message.chat.id, 'en')
    await bot.send_message(message.chat.id,
                           languages.get_status(flag, LANGUAGES.get(first_lang, 'English'), LANGUAGES.get(
                               second_lang, 'English')))


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

    await bot.send_message(message.chat.id, send.text)


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
