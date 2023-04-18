import logging
from telegram.ext import Application, CallbackContext, Updater
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
from telegram import ReplyKeyboardMarkup
from checking_dates import reminder
from load_subjects import load_subjects
from datetime import time


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)


async def start(update, context):
    user = update.effective_user
    session = db_session.create_session()
    have_id = session.query(User).filter(User.telegram_id == user.id).all()
    if not have_id:
        session.add(User(telegram_id=user.id))
        session.commit()
    reply_keyboard = [['/help', '/add'],
                      ['/set_time', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_html(f"""Привет, {user.first_name}. Это бот-напоминалка об олимпидах.
Если нужна помощь, читай /help :)""", reply_markup=markup)


async def help(update, context):
    await update.message.reply_html(f"""Этот бот умеет:
    
/find - найти олимпиады по фильтрам;
/set_time - устаноить время уведомлений;
/add - добавление олимпиады в напоминания;
/own_olimpiad - добавить своё напоминание;
/set_class - установить класс;
/stop - прервать процесс.""")


async def adding(update, context):
    reply_keyboard = [['/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_html("Введите название олимпиады", reply_markup=markup)
    return 1


async def stop(update, context):
    reply_keyboard = [['/help', '/add'],
                      ['/set_time', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_html("Процесс прерван", reply_markup=markup)
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
        reply_keyboard = [['/help', '/add'],
                          ['/set_time', '/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_html("""Олимпиад не найдено""", reply_markup=markup)
    return ConversationHandler.END


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
        await query.answer(f'"{session.query(Olimp.name).filter(Olimp.id == variant).first()[0]}" успешно добавлена в напоминания')





def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def check_dates(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    chat = update.effective_chat
    remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_daily(print_dates, time=time(hour=14, minute=1, second=00), chat_id=chat_id, user_id=user_id)


async def print_dates(context):
    for i in reminder(context.job.user_id):
        await context.bot.send_message(chat_id=context.job.chat_id, text=i)


async def unset(update, context):
    """Удаляет задачу, если пользователь передумал"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)




def main():
    db_session.global_init("db/relations.db")
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(entry_points=[CommandHandler('add', adding)],
                                       states={1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)]},
                                       fallbacks=[CommandHandler('stop', stop)])

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("set", check_dates))
    application.add_handler(CommandHandler("unset", unset))
    application.add_handler(CommandHandler("print_dates", print_dates))
    application.add_handler(conv_handler)
    application.run_polling()



if __name__ == '__main__':
    main()