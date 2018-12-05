import os

import db
import main


def check_auth(login, password):
    db.dbase.connect()

    items = db.Users.get_or_none((db.Users.login == login) & (db.Users.password == password))

    db.dbase.close()

    return items


def get_ttn_fromdb():
    db.dbase.connect()

    try:
        items = db.Ttn.select()
    except db.OperationalError:
        db.Ttn.create_table()
        items = None

    return items


def parsing():
    main.start()


def get_settings(path):
    with open(path+"/alter.ini") as file1:
        alter = file1.read()

    with open(path+"/code.ini") as file2:
        code = file2.read()
    list_files = [file for file in os.listdir(path) if file.endswith(".json")]
    return alter, code, list_files


def save_to_file(val, file):
    with open(file, "w") as f:
        f.write(val)
