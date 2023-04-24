from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import ReplyKeyboardMarkup


async def finding(update, context):  # функция поиска
    reply_markup = [['/stop']]
    markup = ReplyKeyboardMarkup(reply_markup)  # панель команд
    await context.bot.send_message(text='Поиск олимпиады', chat_id=update.effective_chat.id, reply_markup=markup)
    keyboard = [
        [InlineKeyboardButton("По классу", callback_data='class*0')],
        [InlineKeyboardButton("По предмету", callback_data='subject*0')],
        [InlineKeyboardButton("По названию", callback_data='name*0')]
    ]
    markup2 = InlineKeyboardMarkup(keyboard)  # кнопки выбора категории
    await context.bot.send_message(text='По какому критерию делать поиск?', reply_markup=markup2,
                                   chat_id=update.effective_chat.id)  # вывод сообщения

    return 1
