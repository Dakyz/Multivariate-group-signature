import sqlite3
import pickle
from src.constants import Constants

class GroupStore:

    def __init__(self):
        self.connection = sqlite3.connect(Constants.DB_NAME)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            """
            create table IF NOT EXISTS COMPANIES (
            
            -- company id
            id integer primary key,
            
            -- serialized one time key
            R BLOB,
            
            -- serialized secret key
            S BLOB,
            
            -- group signature
            g BLOB,
            
            -- serialized one time key
            t BLOB,
            
            -- hash
            E blob
            )
            """
        )
        self.connection.commit()

    def update_R(self, id, R):
        self.cursor.execute(
            'update COMPANIES set R = ? where id=?',
            (
                pickle.dumps(R),
                id
            )
        )
        self.connection.commit()

    def update_S(self, id, S):
        self.cursor.execute(
            'update COMPANIES set S = ? where id=?',
            (
                pickle.dumps(S),
                id
            )
        )
        self.connection.commit()

    def update_g(self, id, g):
        self.cursor.execute(
            'update COMPANIES set g = ? where id=?',
            (
                pickle.dumps(g),
                id
           )
        )
        self.connection.commit()

    def update_t(self, id, t):
        self.cursor.execute(
            'update COMPANIES set t = ? where id=?',
            (
                pickle.dumps(t),
                id
           )
        )
        self.connection.commit()

    def update_E(self, id, E):
        self.cursor.execute(
            'update COMPANIES set E = ? where id=?',
            (
                pickle.dumps(E),
                id
           )
        )
        self.connection.commit()

    def add_company(self, id, R, S, g, t, E):
        try:
            self.cursor.execute(
                'insert into COMPANIES (id, R, S, g, t, E) values (?, ?, ?, ?, ?, ?)',
                (
                    id,
                    pickle.dumps(R),
                    pickle.dumps(S),
                    pickle.dumps(g),
                    pickle.dumps(t),
                    pickle.dumps(E),
                )
            )
        except sqlite3.IntegrityError:
            print(f"Company {id} is already in db")
        self.connection.commit()

    def get_E(self, id):
        return pickle.loads(
            self.cursor.execute(
                'select E from COMPANIES where id=?',
                (
                    id,
                )
            ).fetchone()[0]
        )

    def get_t(self, id):
        return pickle.loads(
            self.cursor.execute(
                'select t from COMPANIES where id=?',
                (
                    id,
                )
            ).fetchone()[0]
        )

    def get_R(self, id):
        return pickle.loads(
            self.cursor.execute(
                'select R from COMPANIES where id=?',
                (
                    id,
                )
            ).fetchone()[0]
        )

    def get_S(self, id):
        return pickle.loads(
            self.cursor.execute(
                'select S from COMPANIES where id=?',
                (
                    id,
                )
            ).fetchone()[0]
        )

    def get_g(self, id):
        return pickle.loads(
            self.cursor.execute(
                'select g from COMPANIES where id=?',
                (
                    id,
                )
            ).fetchone()[0]
        )

    def update(self, R, S, g):
        self.cursor.execute(
            'update COMPANIES set R = ? where id=?',
            (
                pickle.dumps(R),
                id
            )
        )
        self.cursor.execute(
            'update COMPANIES set S = ? where id=?',
            (
                pickle.dumps(S),
                id
            )
        )
        self.cursor.execute(
            'update COMPANIES set g = ? where id=?',
            (
                pickle.dumps(g),
                id
            )
        )
        self.connection.commit()

    def __delete__(self, instance):
        self.connection.close()