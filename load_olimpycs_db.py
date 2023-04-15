from main import get_olimpiads
import asyncio
from data.db_session import create_session, global_init
from data.olimpics import Olimp
from data.subjects import Subject
from data.olimp_subject import Olimp_Subject


def new_olimpycs():
    session = create_session()
    for i in get_olimpiads():
        if not session.query(Olimp).filter(Olimp.name == i[0]).all():
            session.add(Olimp(name=i[0]))
            session.commit()
            for j in i[1]:
                session.add(Olimp_Subject(olimp=session.query(Olimp.id).filter(Olimp.name == i[0]).first()[0],
                                          subject=session.query(Subject.id).filter(Subject.name == j.lower()).first()[0]))
                session.commit()



