from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import random
from sqlalchemy.sql import select
import db

engine = create_engine('sqlite:///bot.db', echo=True)
meta = MetaData()

users = db.users


def insert(user_id, user_name, group, telegram, date_time,shars):
    ins = users.insert().values(user_id=user_id,
                                user_name=user_name,
                                group=group,
                                shars=shars,
                                telegram=telegram,
                                date_time=date_time)
    conn = engine.connect()
    result = conn.execute(ins)
#    print(result)


def get_all():
    mass = []
    get = users.select()
    conn = engine.connect()
    result = conn.execute(get)
    for row in result:
        mass.append(row)
    # print(mass)
    return mass


def where_user(user_id):
    s = select([users]).where(users.c.user_id == user_id)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    if row is None:
        return True
    else:
        return False


def user_valid(user_name, group):
    s = select([users]).where(users.c.user_name == user_name)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    if row is None:
        return True
    else:
        if row[3] != group:
            return True
        else:
            return False

def get_user(user_id):
    s = select([users]).where(users.c.user_id == user_id)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    return row

# if where_user():
#     print("True")
# else:
#     print("False")


# insert(user_id="345678322", user_name="John Baiden", group="S", telegram="@dolya", date_time="12.12.21 10:41")
# insert(user_id="567890678", user_name="Syan Liny", group="S", telegram="@sapogir", date_time="12.12.21 10:23")
# insert(user_id="754567384", user_name="Dangeon Master", group="S", telegram="@slaves", date_time="12.12.21 10:32")
# insert(user_id="526378212", user_name="Sergio Solomi", group="S", telegram="@damasl", date_time="12.12.21 10:36")
