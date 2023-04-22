from telegram import ReplyKeyboardMarkup


async def unsetting(update, context):
    reply_keyboard = [['/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_html("Введите название олимпиады, которую хотите удалить из напоминаний",
                                    reply_markup=markup)
    return 1