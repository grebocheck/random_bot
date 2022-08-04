from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, delete, update
import db
from sqlalchemy.sql import select

engine = create_engine('sqlite:///bot.db', echo=True)
meta = MetaData()

winer = db.winer


def insert(shara_id, user_id, user_name, group, telegram, date_time):
    ins = winer.insert().values(shara_id=shara_id,
                                user_id=user_id,
                                user_name=user_name,
                                group=group,
                                telegram=telegram,
                                date_time=date_time)
    conn = engine.connect()
    result = conn.execute(ins)
    print(result)


def get_all():
    mass = []
    get = winer.select()
    conn = engine.connect()
    result = conn.execute(get)
    for row in result:
        mass.append(row)
    # print(mass)
    return mass


def use_valdator(shara_id, user_name):
    s = select([winer]).where(winer.c.user_name == user_name).where(winer.c.shara_id == shara_id)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    if row is None:
        return True
    else:
        return False
