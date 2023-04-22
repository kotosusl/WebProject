from telegram.ext import ConversationHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from data import db_session
from data.olimpics import Olimp
from data.subjects import Subject
from telegram import ReplyKeyboardMarkup
from random import shuffle
from data.olimp_subject import Olimp_Subject


async def finding_response(update, context):
    session = db_session.create_session()
    txt = update.message.text
    if context.user_data['status'] == 'class*0':
        if txt.isdigit():
            lst = session.query(Olimp).filter(Olimp.min_class <= int(txt), Olimp.max_class >= int(txt)).all()
            if lst:
                shuffle(lst)
                if len(lst) > 24:
                    lst = lst[:24]
                reply_keyboard = [['/help', '/start'],
                                  ['/find', '/add'],
                                  ['/unset', '/unset_all']]
                markup2 = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
                keys = [[InlineKeyboardButton(f'{j + 1}', callback_data=f'{lst[j].id}*find') for j in range(i, i + 3)]
                        for i in range(0, len(lst) - len(lst) % 3, 3)]
                if len(lst) % 3 != 0:
                    keys.append([InlineKeyboardButton(f'{i + 1}', callback_data=f'{lst[i].id}*find')
                                 for i in range(len(lst) // 3 * 3, len(lst))])
                markup = InlineKeyboardMarkup(keys)
                await update.message.reply_html('Найдены следующие олимпиады:\n\n' +
                                                '\n'.join([f'{i + 1}. {p.name}' for i, p in enumerate(lst)]),
                                                reply_markup=markup)
                await update.message.reply_html('Чтобы больше узнать об олимпиаде, нажмите на её номер',
                                                reply_markup=markup2)
            else:
                reply_keyboard = [['/help', '/start'],
                                  ['/find', '/add'],
                                  ['/unset', '/unset_all']]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
                await update.message.reply_html('Олимпиад не найдено', reply_markup=markup)
        else:
            reply_keyboard = [['/help', '/start'],
                              ['/find', '/add'],
                              ['/unset', '/unset_all']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            await update.message.reply_html('Олимпиад не найдено', reply_markup=markup)
    if context.user_data['status'] == 'subject*0':
        subject_id = session.query(Subject).filter(Subject.name.like(f'%{txt.lower()}%')).all()
        if subject_id:
            subject_id = subject_id[0].id
            lst = session.query(Olimp_Subject).filter(Olimp_Subject.subject == subject_id).all()
            if lst:
                shuffle(lst)
                if len(lst) > 24:
                    lst = lst[:24]
                reply_keyboard = [['/help', '/start'],
                                  ['/find', '/add'],
                                  ['/unset', '/unset_all']]
                markup2 = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
                keys = [[InlineKeyboardButton(f'{j + 1}', callback_data=f'{lst[j].id}*find') for j in range(i, i + 3)]
                        for i in range(0, len(lst) - len(lst) % 3, 3)]
                if len(lst) % 3 != 0:
                    keys.append([InlineKeyboardButton(f'{i + 1}', callback_data=f'{lst[i].id}*find')
                                 for i in range(len(lst) // 3 * 3, len(lst))])
                markup = InlineKeyboardMarkup(keys)
                olimp_txt = '\n'.join([f'{i + 1}. {session.query(Olimp.name).filter(p.olimp == Olimp.id).first()[0]}'
                                       for i, p in enumerate(lst)])
                await update.message.reply_html('Найдены следующие олимпиады:\n\n' + olimp_txt, reply_markup=markup)
                await update.message.reply_html('Чтобы больше узнать об олимпиаде, нажмите на её номер',
                                                reply_markup=markup2)
            else:
                reply_keyboard = [['/help', '/start'],
                                  ['/find', '/add'],
                                  ['/unset', '/unset_all']]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
                await update.message.reply_html('Олимпиад не найдено', reply_markup=markup)
        else:
            reply_keyboard = [['/help', '/start'],
                              ['/find', '/add'],
                              ['/unset', '/unset_all']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            await update.message.reply_html('Олимпиад не найдено', reply_markup=markup)
    if context.user_data['status'] == 'name*0':
        lst = session.query(Olimp).filter(Olimp.name.like(f'%{txt.lower()}%')).all()
        if lst:
            shuffle(lst)
            if len(lst) > 24:
                lst = lst[:24]
            reply_keyboard = [['/help', '/start'],
                              ['/find', '/add'],
                              ['/unset', '/unset_all']]
            markup2 = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            keys = [[InlineKeyboardButton(f'{j + 1}', callback_data=f'{lst[j].id}*find') for j in range(i, i + 3)]
                    for i in range(0, len(lst) - len(lst) % 3, 3)]
            if len(lst) % 3 != 0:
                keys.append([InlineKeyboardButton(f'{i + 1}', callback_data=f'{lst[i].id}*find')
                             for i in range(len(lst) // 3 * 3, len(lst))])
            markup = InlineKeyboardMarkup(keys)
            await update.message.reply_html('Найдены следующие олимпиады:\n\n' +
                                            '\n'.join([f'{i + 1}. {p.name}' for i, p in enumerate(lst)]),
                                            reply_markup=markup)
            await update.message.reply_html('Чтобы больше узнать об олимпиаде, нажмите на её номер',
                                            reply_markup=markup2)
        else:
            reply_keyboard = [['/help', '/start'],
                              ['/find', '/add'],
                              ['/unset', '/unset_all']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            await update.message.reply_html('Олимпиад не найдено', reply_markup=markup)
    return ConversationHandler.END
