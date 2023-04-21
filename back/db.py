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
                d.execute(text_for_execute, params).fetchall()
            else:
                d.execute(text_for_execute, params)
                d.commit()

    def creating_tables(self):
        self.con(""" CREATE TABLE IF NOT EXISTS people_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(32),
        surname VARCHAR(32),
        email VARCHAR(32) NOT NULL,
        password VARCHAR(32) NOT NULL 
        );""")

    def crate_recorts(self, name: str, surnmae: str, email: str, password: str):
        f = self.con('SELECT id+1 FROM peoples_data ORDER BY id DESK LIMIT 1;', fetchall=True)
        f = 0 if f == [] else f[0][0]
        self.con(""" INSERT INTO peoples_data (name, surname, email, password) VALUES(?, ?, ?, ?);""",
                 params=(name, surnmae, email, password))

    def get_values(self):
        values = self.con('SELECT * FORM peoples_data WHERE id=?', params=(id,), off=True, fetchall=False)

        return values


s = Database('database.db')

