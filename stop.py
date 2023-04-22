from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup


async def stop(update, context):
    reply_keyboard = [['/help', '/start'],
                      ['/find', '/add'],
                      ['/unset', '/unset_all']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_html("Действие отменено", reply_markup=markup)
    return ConversationHandler.END
