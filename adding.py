from telegram import ReplyKeyboardMarkup


async def adding(update, context):  # запуск функции добавления олимпиады
    reply_keyboard = [['/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)  # панель с командами
    await update.message.reply_html("Введите название олимпиады, которую хотите добавить", reply_markup=markup)
    # вывод сообщения
    return 1
