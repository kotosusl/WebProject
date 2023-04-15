import logging
from telegram.ext import Application
from TOKEN import TOKEN
from datetime import datetime
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from data import db_session
from data.users import User
from data.olimpics import Olimp
from data.user_olimpyc import Relation
from main import get_olimpiads
from data.subjects import Subject
from load_olimpycs_db import new_olimpycs


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)


async def start(update, context):
    user = update.effective_user
    session = db_session.create_session()
    have_id = session.query(User).filter(User.telegram_id == user.id).all()
    if not have_id:
        session.add(User(telegram_id=user.id))
        session.commit()

    await update.message.reply_html(f"""Привет, {user.first_name}. Это бот-напоминалка об олимпидах.
Если нужна помощь, читай /help :)""")


async def help(update, context):
    await update.message.reply_html(f"""Этот бот умеет:
    
/find - найти олимпиады по фильтрам;
/set_time - устаноить время уведомлений;
/add - добавление олимпиады в напоминания;
/own_olimpiad - добавить своё напоминание;
/set_class - установить класс;
/stop - прервать процесс.""")


async def find(update, context):
    await update.message.reply_html("Введите название олимпиады")
    return 1


async def stop(update, context):
    await update.message.reply_html("Процесс прерван")
    return ConversationHandler.END


async def first_response(update, context):
    olimp = update.message.text
    session = db_session.create_session()
    result = session.query(Olimp).filter(Olimp.name.like(f'%{olimp}%')).all()
    if result:
        keys = [[InlineKeyboardButton(f'{j + 1}', callback_data=f'{result[j].id}') for j in range(i, i + 3)]
                for i in range(0, len(result) - len(result) % 3, 3)]
        if len(result) % 3 != 0:
            keys.append([InlineKeyboardButton(f'{i + 1}', callback_data=f'{result[i].id}')
                         for i in range(len(result) // 3 * 3, len(result))])
        markup = InlineKeyboardMarkup(keys)
        await update.message.reply_html("""Найдены следующие олимпиады:\n\n""" +
                                        '\n'.join([f'{i + 1}. {p.name}' for i, p in enumerate(result)]) +
                                        '\n\nДля добавления олимпиады в список напоминаний выберите номер',
                                        reply_markup=markup)
    else:
        await update.message.reply_html("""Олимпиад не найдено""")
    return 2


async def button(update, _):
    query = update.callback_query
    variant = query.data

    session = db_session.create_session()
    self_id = session.query(User).filter(User.telegram_id == update.effective_user.id).first()
    if session.query(Relation).filter(Relation.user == self_id.id, Relation.olimp == variant).all():
        await query.answer("Олимпиада уже добавлена в напоминания")
    else:
        session.add(Relation(user=self_id.id, olimp=variant))
        session.commit()
        await query.answer(f'Олимпиада "{session.query(Olimp.name).filter(Olimp.id == variant).first()[0]}" успешно добавлена в напоминания')


def main():
    db_session.global_init("db/relations.db")
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(entry_points=[CommandHandler('find', find)],
                                       states={1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)]},
                                       fallbacks=[CommandHandler('stop', stop)])

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()