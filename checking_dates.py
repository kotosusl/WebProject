from data import db_session
from data.users import User
from data.user_olimpyc import Relation
from data.olimpics import Olimp
from datetime import date, timedelta
from data.olimp_dates import Olimp_dates
from data.olimp_subject import Olimp_Subject
from data.subjects import Subject


def reminder(user):  # проверка дат олимпиад
    session = db_session.create_session()
    user_id = session.query(User.id).filter(User.telegram_id == user).first()[0]
    user_list = session.query(Relation.olimp).filter(Relation.user == user_id).all()
    list_olimpiads = []
    for i in user_list:  # перебор всех олимпиад пользователя
        olimp = session.query(Olimp).filter(Olimp.id == i[0]).first()
        olimp_data = session.query(Olimp_dates).filter(Olimp_dates.olimp == i[0]).all()
        for j in olimp_data:  # проверка дат этапов олимпиады
            if (j.start_date == timedelta(days=3) + date.today() or j.start_date == date.today() or
                    (date.today() + timedelta(days=3) == j.end_date and j.end_date - j.start_date > timedelta(days=3))):
                if j.start_date == timedelta(days=3) + date.today():  # при совпадении сроков формирование сообщения
                    text = f"""Через три дня начинается {j.event.lower()} в мероприятии "{olimp.name}"!\n\n"""
                elif j.start_date == date.today():
                    text = f"""Уже сегодня начинается {j.event.lower()} в мероприятии "{olimp.name}"!\n\n"""
                else:
                    text = f"""Осталось три дня и {j.event.lower()} в мероприятии "{olimp.name}" закончится!\n\n"""
                subjects = session.query(Olimp_Subject.subject).filter(Olimp_Subject.olimp == i[0]).all()
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
                list_olimpiads.append(text)  # добабление в список сообщений
    return list_olimpiads
