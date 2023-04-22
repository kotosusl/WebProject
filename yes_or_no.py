from telegram.ext import ConversationHandler
from data import db_session
from data.users import User
from data.user_olimpyc import Relation


async def yes_or_no(update, _):
    query = update.callback_query
    txt = query.data
    if txt == 'yes*0':
        session = db_session.create_session()
        user_id = session.query(User.id).filter(User.telegram_id == query.from_user.id).first()[0]
        session.query(Relation).filter(Relation.user == user_id).delete()
        session.commit()
        await query.answer(text="Все уведомления удалены")
    else:
        await query.answer(text="Действие отменено")
    return ConversationHandler.END
