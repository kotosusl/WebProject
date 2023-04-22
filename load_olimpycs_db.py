from main import get_olimpiads
import asyncio
from data.db_session import create_session, global_init
from data.olimpics import Olimp
from data.subjects import Subject
from data.olimp_subject import Olimp_Subject
from data.olimp_dates import Olimp_dates
from datetime import date, timedelta


def new_olimpycs():
    session = create_session()
    for i in get_olimpiads():
        if not session.query(Olimp).filter(Olimp.name == i[0]).all():
            session.add(Olimp(name=i[0], desc=i[2], href=i[3], min_class=i[9], max_class=i[10]))
            session.commit()

            for j in i[1]:
                session.add(Olimp_Subject(olimp=session.query(Olimp.id).filter(Olimp.name == i[0]).first()[0],
                                          subject=session.query(Subject.id).filter(Subject.name == j.lower()).first()[
                                              0]))
                session.commit()

            for k in range(4, 9):
                for j in i[k]:
                    first_day = j['date'].split('-')
                    session.add(Olimp_dates(olimp=session.query(Olimp.id).filter(Olimp.name == i[0]).first()[0],
                                            start_date=date(int(first_day[0]), int(first_day[1]), int(first_day[2])),
                                            end_date=date(int(first_day[0]), int(first_day[1]),
                                                          int(first_day[2])) + timedelta(days=int(j['length'])),
                                            event=j.find('span', class_='tl_cont_f').find('font').get_text()))
                    session.commit()
