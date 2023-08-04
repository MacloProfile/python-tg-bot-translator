from googletrans import Translator, LANGUAGES
from telebot.async_telebot import AsyncTeleBot
import asyncio
from telebot.types import InlineQuery, InputTextMessageContent
from telebot import types

# Create a dictionary to store the selected target language for each user
user_language = {}

bot = AsyncTeleBot("6341597101:AAGMGE6l5cXEU37JlChhvSP5gopt-Algxd0", parse_mode=None)

# Handler for the /start command
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message,'Hello, '
                            + message.from_user.first_name)

# Handler for the /help command
@bot.message_handler(commands=['help'])
async def send_welcome(message):
    await bot.reply_to(message,'Just enter text and hit send\n'
                            + "I'll figure out what language it is."
                            + "If it doesn't translate, try again."
                            + 'Google translate')

# Handler for the /setlang command
@bot.message_handler(commands=['setlang'])
async def set_language(message):
    try:
        lang_code = message.text.split(' ', 1)[1].lower()
        # Check that the selected language exists, otherwise we use English (default)
        if lang_code in LANGUAGES:
            user_language[message.chat.id] = lang_code
            await bot.reply_to(message, 'Language selected: ' + LANGUAGES[lang_code])
        else:
            await bot.reply_to(message, 'Incorrect language. The default English is used.')
    except IndexError:
        await bot.reply_to(message, 'Command usage: /setlang language')

# Text message handler
@bot.message_handler()
async def user_text(message):
    translator = Translator()

    # Define the input language or use the selected translation language
    if message.chat.id in user_language:
        lang = user_language[message.chat.id]
    else:
        lang = translator.detect(message.text).lang

    # Translate the text into the selected target language
    send = translator.translate(message.text, dest=lang)
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
    if message.chat.id in user_language:
        lang = user_language[message.chat.id]
    else:
        lang = translator.detect(caption).lang

    # Translate the caption into the selected target language
    send = translator.translate(caption, dest=lang)
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
    if query.from_user.id in user_language:
        lang = user_language[query.from_user.id]
    else:
        lang = translator.detect(text).lang

    # Translate the text into the selected target language
    send = translator.translate(text, dest=lang)
    results.append(types.InlineQueryResultArticle(
        id='1', title=send.text, input_message_content=types.InputTextMessageContent(
            message_text=send.text)))

    await bot.answer_inline_query(query.id, results)

# Run and re-run on failure.
asyncio.run(bot.infinity_polling())
