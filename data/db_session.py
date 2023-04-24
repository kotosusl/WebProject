import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()  # абстрактная декларативная база

__factory = None  # для получения сессий подключения к бд


def global_init(db_file):  # инициализация базы данных
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():  # проверка указания бд
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'  # путь до бд
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)  # движок для работы с бд
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)  # создать все несозданные объекты бд


def create_session() -> Session:  # получение сессий подключения
    global __factory
    return __factory()
