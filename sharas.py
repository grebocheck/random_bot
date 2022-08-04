from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, delete, update
from sqlalchemy.sql import select
import random
import db

engine = create_engine('sqlite:///bot.db', echo=True)
meta = MetaData()

shara = db.shara


def insert(description, groups, amount):
    ins = shara.insert().values(description=description,
                                groups=groups,
                                amount=amount)
    conn = engine.connect()
    result = conn.execute(ins)
    print(result)


def delete_shara(shara_id):
    dele = delete(shara).where(shara.c.shara_id == shara_id)
    conn = engine.connect()
    result = conn.execute(dele)
    print(result)


def get_all():
    mass = []
    get = shara.select()
    conn = engine.connect()
    result = conn.execute(get)
    for row in result:
        mass.append(row)
    # print(mass)
    return mass


def update_shara(shara_id, description, groups, amount):
    upd = update(shara).where(shara.c.shara_id == shara_id).values(shara_id=shara_id,
                                                                   description=description,
                                                                   groups=groups,
                                                                   amount=amount)
    conn = engine.connect()
    result = conn.execute(upd)
    print(result)


def shara_in_group(group):
    mass = []
    shara_mass = get_all()
    for a in range(len(shara_mass)):
        if group in shara_mass[a][2].split(' '):
            mass.append(shara_mass[a][0])
    return mass


def shara_select(shara_id):
    mass = []
    get = shara.select().where(shara.c.shara_id == shara_id)
    conn = engine.connect()
    result = conn.execute(get)
    for row in result:
        mass.append(row)
    # print(mass)
    return mass[0]


def shara_num_valid(shara_id):
    get = shara.select().where(shara.c.shara_id == shara_id)
    conn = engine.connect()
    result = conn.execute(get)
    row = result.fetchone()
    if row is None:
        return False
    else:
        return True