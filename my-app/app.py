import os
import json

from flask import Flask, request
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.sql.expression import exists

app = Flask(__name__)

config = {
    'DATABASE_URI': os.environ.get('DATABASE_URI', ''),
    'HOSTNAME': os.environ['HOSTNAME'],
    'GREETING': os.environ.get('GREETING', 'Hello'),
}

@app.route("/")
def hello():
    return config['GREETING'] + ' from ' + config['HOSTNAME'] + '!'

@app.route("/config")
def configuration():
    # config['version'] = 'NEW'
    return json.dumps(config)

@app.route('/users')
def users():
    engine = create_engine(config['DATABASE_URI'], echo=True)
    rows = []
    with engine.connect() as connection:
        result = connection.execute("select username, firstname, lastname, email, phone from users")
        rows = [dict(r.items()) for r in result]
    return json.dumps(rows)

@app.route('/user', methods=['POST'])
def add_user():
    _json = request.json
    _username = _json['username']
    _firstname = _json['firstname']
    _lastname = _json['lastname']
    _email = _json['email']
    _phone = _json['phone']
    engine = create_engine(config['DATABASE_URI'], echo=True)
    meta = MetaData()
    users = Table(
        'users', meta,
        Column('id', Integer, primary_key = True),
        Column('username', String),
        Column('firstname', String),
        Column('lastname', String),
        Column('email', String),
        Column('phone', String),
    )
    ins = users.insert()
    ins = users.insert().values(username = _username, firstname = _firstname, lastname = _firstname, email = _email, phone = _phone)
    conn = engine.connect()
    result = conn.execute(ins)
    return "User added successfully!"

@app.route('/user/<int:user_id>')
def user(user_id):
    engine = create_engine(config['DATABASE_URI'], echo=True)
    meta = MetaData()
    users = Table(
        'users', meta,
        Column('id', Integer, primary_key = True),
        Column('username', String),
        Column('firstname', String),
        Column('lastname', String),
        Column('email', String),
        Column('phone', String),
    )
    conn = engine.connect()
    s = users.select().where(users.c.id == user_id)
    result = conn.execute(s)

    rows = [dict(r.items()) for r in result]
    return json.dumps(rows)

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    _json = request.json
    _username = _json['username']
    _firstname = _json['firstname']
    _lastname = _json['lastname']
    _email = _json['email']
    _phone = _json['phone']

    engine = create_engine(config['DATABASE_URI'], echo=True)
    meta = MetaData()
    users = Table(
        'users', meta,
        Column('id', Integer, primary_key = True),
        Column('username', String),
        Column('firstname', String),
        Column('lastname', String),
        Column('email', String),
        Column('phone', String),
    )
    conn = engine.connect()
    stmt=users.update().where(users.c.id==user_id).values(username = _username, firstname = _firstname, lastname = _firstname, email = _email, phone = _phone)
    conn.execute(stmt)
    return "User update successfully!"

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    engine = create_engine(config['DATABASE_URI'], echo=True)
    meta = MetaData()
    users = Table(
        'users', meta,
        Column('id', Integer, primary_key = True),
        Column('username', String),
        Column('firstname', String),
        Column('lastname', String),
        Column('email', String),
        Column('phone', String),
    )
    conn = engine.connect()
    stmt=users.delete().where(users.c.id==user_id)
    conn.execute(stmt)
    return "User deleted successfully!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80', debug=True)