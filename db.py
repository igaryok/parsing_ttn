from peewee import Model, SqliteDatabase, CharField, IntegerField, OperationalError


dbase = SqliteDatabase("data/check_ttn.db")


class Users(Model):
    class Meta:
        database = dbase
        db_table = "users"

    login = CharField()
    password = CharField()


class Ttn(Model):
    class Meta:
        database = dbase
        db_table = "ttn"

    number = CharField()
    status_text = CharField()
    status_symbol = CharField()
    row_in_sheet = IntegerField()


def find_ttn(ttn):
    dbase.connect()
    find_ttn = Ttn.get_or_none(Ttn.number == ttn)
    dbase.close()
    return find_ttn


def write_newttn(ttn, status_s, row):
    dbase.connect()
    Ttn.create(number=ttn,
               satus_text="",
               status_symbol=status_s,
               row_in_sheet=row)
    dbase.close()


def write_status_db(ttn, status_t, status_s, row):
    dbase.connect()
    find_ttn = Ttn.get_or_none(Ttn.number == ttn)
    if find_ttn:
        find_ttn.status_text = status_t
        find_ttn.status_symbol = status_s
        find_ttn.row_in_sheet = row
        find_ttn.save()
    else:
        Ttn.create(number=ttn,
                   satus_text=status_t,
                   status_symbol=status_s,
                   row_in_sheet=row)
    dbase.close()
