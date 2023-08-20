# List of most popular languages
MOST_POPULAR_LANGUAGES = [
    'en - English',
    'ru - Russian',
    'es - Spanish',
    'fr - French',
    'de - German',
    'zh-CN - Chinese (Simplified)',
    'it - Italian',
    'pt - Portuguese',
    'ja - Japanese'
]


def get_available_commands(num):
    if num == "0":
        return 'Available commands for the bot:\n' + '/start - Start the bot\n' + '/help - how to use the bot\n' +'/first en - Set the first translation language\n' + '/second en - Set the second translation language\n' + '/languages - Show the list of languages\n' + '/status - Show the selected languages for translation'
    elif num == "1":
        return 'Доступные команды для бота:\n' + '/start - Запустить бота\n' + '/help - как пользоваться ботом\n' + '/first en - Установить первый язык перевода\n' + '/second en - Установить второй язык перевода\n' + '/languages - Показать список языков\n' + '/status - Показать выбранные языки для перевода'


def get_start_info(num):
    if num == "0":
        return "Set the main language to translate to (/first en/ru/es/de/it...).\n\n " + "If the language of the user's message is the same as the primary language, the bot will translate messages into the second language \n" + "/first en - Set the primary language of the translation \n" + "/second uk - Set an additional language of translation (optional)\n\n\n"\
               + "EXAMPLE: the main language is English, the second language is Spanish. Below are the following lines of the communication-translation type\n" \
               + "me encanta la pizza = I love pizza\n" \
               + "I love pizza = me encanta la pizza\n" \
               + "ピザが大好きです = i love pizza\n\n" \
               + 'Most popular languages for translation (for a complete list, type /languages):\n' + '\n'.join(
            MOST_POPULAR_LANGUAGES)
    elif num == "1":
        return "Установите основной язык на который переводить (/first en/ru/es/de/it...).\n\n" + "Если язык сообщения пользователя совпадает с основным языком, от бот переведет сообщения на дополнительный язык \n" + "/first en - Установка основного языка перевода\n" + "/second uk - Установка дополнительного языка перевода (не обязательно)\n\n"\
	       + "ПРИМЕР: основной язык - Английский, второй - Испанский. Ниже приведены строчки типа сообщение - перевод\n" \
	       + "me encanta la pizza = I love pizza\n"\
               + "I love pizza = me encanta la pizza\n"\
               + "ピザが大好きです = i love pizza\n\n"\
               + 'Самые популярные языки для перевода (для получения полного списка введите /languages):\n' + '\n'.join(
            MOST_POPULAR_LANGUAGES)


def get_status(num, name1, name2):
    if num == "0":
        return 'First translation language: ' + name1 + '\n' + 'Second translation language: ' + name2
    elif num == "1":
        return 'Первый язык перевода: ' + name1 + '\n' + 'Второй язык перевода: ' + name2
