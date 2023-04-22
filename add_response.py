from telegram.ext import ConversationHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from data import db_session
from data.olimpics import Olimp
from telegram import ReplyKeyboardMarkup


async def add_response(update, context):
    olimp = update.message.text
    session = db_session.create_session()
    result = session.query(Olimp).filter(Olimp.name.like(f'%{olimp}%')).all()
    if result:
        if len(result) <= 24:
            keys = [[InlineKeyboardButton(f'{j + 1}', callback_data=f'{result[j].id}*add') for j in range(i, i + 3)]
                    for i in range(0, len(result) - len(result) % 3, 3)]
            if len(result) % 3 != 0:
                keys.append([InlineKeyboardButton(f'{i + 1}', callback_data=f'{result[i].id}*add')
                             for i in range(len(result) // 3 * 3, len(result))])
            markup = InlineKeyboardMarkup(keys)
            reply_keyboard = [['/help', '/start'],
                              ['/find', '/add'],
                              ['/unset', '/unset_all']]
            markup2 = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            await update.message.reply_html("""Найдены следующие олимпиады:\n\n""" +
                                            '\n'.join([f'{i + 1}. {p.name}' for i, p in enumerate(result)]) +
                                            '\n\nДля добавления олимпиады в список напоминаний выберите номер',
                                            reply_markup=markup)
            await update.message.reply_html('Для добавления олимпиады в список напоминаний выберите номер',
                                            reply_markup=markup2)
        else:
            reply_keyboard = [['/help', '/start'],
                              ['/find', '/add'],
                              ['/unset', '/unset_all']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            await update.message.reply_html("""Найдено слишком много олимпиад""", reply_markup=markup)
            return ConversationHandler.END
    else:
        reply_keyboard = [['/help', '/start'],
                          ['/find', '/add'],
                          ['/unset', '/unset_all']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_html("""Олимпиад не найдено""", reply_markup=markup)
    return ConversationHandler.END
