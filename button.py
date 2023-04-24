from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from data import db_session
from data.users import User
from data.olimpics import Olimp
from data.user_olimpyc import Relation
from data.subjects import Subject
from data.olimp_subject import Olimp_Subject


async def button(update, context):  # кнопки
    query = update.callback_query
    variant = query.data  # тип кнопки
    session = db_session.create_session()
    self_id = session.query(User).filter(User.telegram_id == update.effective_user.id).first()
    # определение пользователя
    if variant.split('*')[1] == 'add':  # если кнопка для добавления
        if session.query(Relation).filter(Relation.user == self_id.id, Relation.olimp == variant.split('*')[0]).all():
            await query.answer("Олимпиада уже добавлена в напоминания")  # проверка наличия олимпиады у пользователя
        else:
            session.add(Relation(user=self_id.id, olimp=variant.split('*')[0]))  # добавление олимпиады к пользователю
            session.commit()
            await query.answer(
                f'''"{session.query(Olimp.name).filter(Olimp.id == 
                                                       int(variant.split(
                                                           '*')[0])).first()[0]}" успешно добавлена в напоминания''')

    elif variant.split('*')[1] == 'unset':  # если кнопка для удаления
        if session.query(Relation).filter(Relation.id == int(variant.split('*')[0])).all():
            # проверка наличия оимпиады у пользователя
            olimp = session.query(Relation.olimp).filter(Relation.id == int(variant.split('*')[0])).first()[0]
            session.query(Relation).filter(Relation.id == int(variant.split('*')[0])).delete()
            session.commit()  # удаление олимпиады
            await query.answer(
                f'''"{session.query(Olimp.name).filter(Olimp.id == 
                                                       olimp).first()[0]}" успешно удалена из напоминаний''')
        else:
            await query.answer('Олимпиада уже удалена')
    elif variant.split('*')[1] == 'find':  # если кнопка для поиска
        olimp = session.query(Olimp).filter(Olimp.id == int(variant.split("*")[0])).first()
        text = f'{olimp.name}\n\n'  # формирование сообщения об олимпиаде
        subjects = session.query(Olimp_Subject.subject).filter(Olimp_Subject.olimp == olimp.id).all()
        for num, k in enumerate(subjects):
            if num != 0:
                text += f', {session.query(Subject.name).filter(Subject.id == k[0]).first()[0].capitalize()}'
            else:
                text += f'{session.query(Subject.name).filter(Subject.id == k[0]).first()[0].capitalize()}'
        if olimp.min_class != olimp.max_class:
            text += f'\n\n{olimp.min_class}-{olimp.max_class} класс'
        else:
            text += f'\n\n{olimp.max_class} класс'
        if olimp.desc:
            text += f'\n\n{olimp.desc}'
        text += f'\n\nПодробнее по ссылке:\nhttps://olimpiada.ru{olimp.href}'
        keyboard = [[InlineKeyboardButton('Добавить в напоминания', callback_data=f'{olimp.id}*add')]]
        markup = InlineKeyboardMarkup(keyboard)  # кнопка добавления
        await context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=markup)
        # вывод сообщения
