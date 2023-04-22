from telegram.ext import ConversationHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from data import db_session
from data.users import User
from data.olimpics import Olimp
from data.user_olimpyc import Relation
from telegram import ReplyKeyboardMarkup


async def unset_response(update, context):
    olimp = update.message.text
    session = db_session.create_session()
    user = session.query(User.id).filter(update.effective_user.id == User.telegram_id).first()[0]
    result = session.query(Relation).filter(Relation.user == user).all()
    list_olimpiads = []
    for i in result:
        current = session.query(Olimp).filter(Olimp.id == i.olimp).first()
        if current and olimp.lower() in current.name.lower():
            list_olimpiads.append((current, i.id))

    if list_olimpiads:
        if len(list_olimpiads) <= 24:
            keys = [[InlineKeyboardButton(f'{j + 1}', callback_data=f'{list_olimpiads[j][1]}*unset') for j in
                     range(i, i + 3)]
                    for i in range(0, len(list_olimpiads) - len(list_olimpiads) % 3, 3)]
            if len(list_olimpiads) % 3 != 0:
                keys.append([InlineKeyboardButton(f'{i + 1}', callback_data=f'{list_olimpiads[i][1]}*unset')
                             for i in range(len(list_olimpiads) // 3 * 3, len(list_olimpiads))])
            markup = InlineKeyboardMarkup(keys)
            reply_keyboard = [['/help', '/start'],
                              ['/find', '/add'],
                              ['/unset', '/unset_all']]
            markup2 = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

            await update.message.reply_html("""Найдены следующие олимпиады:\n\n""" +
                                            '\n'.join([f'{i + 1}. {p[0].name}' for i, p in enumerate(list_olimpiads)]),
                                            reply_markup=markup)
            await update.message.reply_html('Для удаления олимпиады из списка выберите номер', reply_markup=markup2)
        else:
            reply_keyboard = [['/help', '/start'],
                              ['/find', '/add'],
                              ['/unset', '/unset_all']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            await update.message.reply_html("""Найдено слишком много олимпиад""", reply_markup=markup)
    else:
        reply_keyboard = [['/help', '/start'],
                          ['/find', '/add'],
                          ['/unset', '/unset_all']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_html("""Олимпиад не найдено""", reply_markup=markup)
    return ConversationHandler.END
