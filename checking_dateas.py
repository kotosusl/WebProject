from main import get_olimpiads
from data import db_session
from data.users import User
from data.user_olimpyc import Relation
from data.olimpics import Olimp


def reminder(user):
    session = db_session.create_session()
    user_id = session.query(User.id).filter(User.telegram_id == user).first()[0]
    user_list = session.query(Relation.olimp).filter(Relation.user == user_id).all()
    for i in user_list:
        olimp_data = get_olimpiads(olimp=session.query(Olimp.name).filter(Olimp.id == i[0]).first()[0])
        print(olimp_data[0])