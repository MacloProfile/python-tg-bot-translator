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
        return "Set the first and second languages with the following commands.\n" + "❗The first language is the primary language. If you enter a phrase and do not specify its ""language, it will be automatically translated into the first language (/first)\n\n ""/first en - Set the primary language for translation\n" + "/second uk - Set the second translation language\n\n" + 'Most popular languages for translation (for a complete list, type /languages):\n' + '\n'.join(
            MOST_POPULAR_LANGUAGES)
    elif num == "1":
        return "Установите первый и второй языки с помощью следующих команд.\n" + "❗Первый язык является основным. Если вы вводите фразу и не указываете ее ""язык, она будет автоматически переведена на первый язык (/first)\n\n ""/first en - Установка основного языка перевода\n" + "/second uk - Установка второго языка перевода\n\n" + 'Самые популярные языки для перевода (для получения полного списка введите /languages):\n' + '\n'.join(
            MOST_POPULAR_LANGUAGES)


def get_status(num, name1, name2):
    if num == "0":
        return 'First translation language: ' + name1 + '\n' + 'Second translation language: ' + name2
    elif num == "1":
        return 'Первый язык перевода: ' + name1 + '\n' + 'Второй язык перевода: ' + name2
