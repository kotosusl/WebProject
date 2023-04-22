from data import db_session
from data.users import User
from telegram import ReplyKeyboardMarkup
from datetime import time
from remove_job_if_exists import remove_job_if_exists
from print_dates import print_dates


async def start(update, context):
    user = update.effective_user
    session = db_session.create_session()
    have_id = session.query(User).filter(User.telegram_id == user.id).all()
    if not have_id:
        session.add(User(telegram_id=user.id))
        session.commit()
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_daily(print_dates, time=time(hour=7, minute=0, second=0), chat_id=chat_id, user_id=user_id)
    reply_keyboard = [['/help', '/start'],
                      ['/find', '/add'],
                      ['/unset', '/unset_all']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_html(f"""Привет, {user.first_name}. Это бот-напоминалка об олимпидах.
Если нужна помощь, читай /help :)""", reply_markup=markup)
