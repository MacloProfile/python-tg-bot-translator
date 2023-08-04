# Import the necessary libraries
from googletrans import Translator, LANGUAGES
from telegram import ReplyKeyboardMarkup

# Dictionaries to store the first and second translation languages for each user
user_translation_language = {}
user_second_translation_language = {}

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

# Function to translate the message based on user's selected languages
def translate_message(message_text, from_lang, to_lang):
    translator = Translator()
    translation = translator.translate(message_text, src=from_lang, dest=to_lang)
    return translation.text

# Function to create the reply keyboard with the "Admin" and "Help" buttons in one row
def create_start_reply_keyboard():
    reply_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    reply_keyboard.add('/admin', '/help')
    return reply_keyboard