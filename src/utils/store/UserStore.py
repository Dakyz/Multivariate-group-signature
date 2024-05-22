from src.constants import Constants
from names_generator import generate_name
import sqlite3
import pickle

class UserStore:

    def __init__(self):
        self.connection = sqlite3.connect(Constants.DB_NAME)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            """
            create table IF NOT EXISTS Users (
            -- user id
            id integer primary key,
            
            -- username
            username text not null,
            
            -- email
            email text not null,
            
            -- serialized secret key
            u BLOB not null
            )
            """
        )
        self.connection.commit()

    def add_user(self, id: int, sk):
        try:
            self.cursor.execute(
                'insert into USERS (id, username, email, u) values (?, ?, ?, ?)',
                (
                    id,
                    generate_name(style='capital', seed=id),
                    f'{generate_name(seed=id)}_{id}@email.com',
                    pickle.dumps(sk)
                )
            )
        except sqlite3.IntegrityError:
            print(f"User {id} is already in db")
        self.connection.commit()

    def update_user_sk(self, id: int, sk):
        self.cursor.execute(
            'update USERS set sk = ? where id=?',
            (
                pickle.dumps(sk),
                id
            )
        )
        self.connection.commit()

    def get_username(self, id):
        return self.cursor.execute(
            'select username from USERS where id=?',
            (
                id,
            )
        ).fetchone()[0]

    def get_user_email(self, id):
        return self.cursor.execute(
            'select email from USERS where id=?',
            (
                id,
            )
        ).fetchone()[0]

    def get_user_sk(self, id):
        return pickle.loads(
            self.cursor.execute(
                'select u from USERS where id=?',
                (
                    id,
                )
            ).fetchone()[0]
        )

    def __delete__(self, instance):
        self.connection.close()