from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

engine = create_engine('sqlite:///bot.db', echo=True)
meta = MetaData()

users = Table(
    'students', meta,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String),
    Column('shars', String),
    Column('group', String),
    Column('telegram', String),
    Column('date_time', String),
)

shara = Table(
    'shara', meta,
    Column('shara_id', Integer, primary_key=True),
    Column('description', String),
    Column('groups', String),
    Column('amount', Integer),
)

winer = Table(
    'winer', meta,
    Column('id', Integer, primary_key=True),
    Column('shara_id', Integer),
    Column('user_id', Integer,),
    Column('user_name', String),
    Column('group', String),
    Column('telegram', String),
    Column('date_time', String),
)


if __name__ == '__main__':
    meta.create_all(engine)
