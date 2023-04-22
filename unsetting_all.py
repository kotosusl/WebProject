from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import ReplyKeyboardMarkup


async def unsetting_all(update, context):
    reply_keyboard = [['/help', '/start'],
                      ['/find', '/add'],
                      ['/unset', '/unset_all']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data='yes*0'),
            InlineKeyboardButton("Нет", callback_data='no*0'),
        ]
    ]
    markup2 = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(text='Удаление всех уведомлений', reply_markup=markup,
                                   chat_id=update.effective_chat.id)
    await context.bot.send_message(text='Вы уверены, что хотите удалить все уведомления?', reply_markup=markup2,
                                   chat_id=update.effective_chat.id)
    return 1
