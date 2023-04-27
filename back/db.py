import sqlite3
from sqlite_plus import sqlite_dict


class Database:
    def __init__(self, name_db):
        self.name_db = name_db

    @sqlite_dict
    def con(self, text_for_execute: str, fetchall: bool = False, params: tuple = ()):
        with sqlite3.connect(self.name_db) as d:
            d.cursor()
            if fetchall:
                return d.execute(text_for_execute, params).fetchall()
            else:
                d.execute(text_for_execute, params)
                d.commit()

    def creating_tables(self):
        self.con(""" CREATE TABLE IF NOT EXISTS peoples_data_reg (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login VARCHAR(32),
        email VARCHAR(32) NOT NULL,
        password VARCHAR(32) NOT NULL 
        );""")

    def crate_recorts_reg(self, login: str, email: str, password: str):
        f = self.con('SELECT id FROM peoples_data_reg ORDER BY id DESC LIMIT 1;', fetchall=True)
        f = 0 if f == [] else f[0][0]
        self.con("INSERT INTO peoples_data_reg (login, email, password) VALUES(?, ?, ?);",
                 params=(login, email, password))

    def get_values(self, login):
        values = self.con('SELECT * FROM peoples_data_reg WHERE login=?', params=(login,), off=False, fetchall=True)
        return values


# s = Database('database.db')
# print(s.get_values())
