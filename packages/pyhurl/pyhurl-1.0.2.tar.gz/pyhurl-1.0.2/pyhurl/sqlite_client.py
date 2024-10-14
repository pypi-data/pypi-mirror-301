import os
import sqlite3
from abc import ABC
from typing import Optional
from dotenv import load_dotenv


class SqliteClient(ABC):
    load_dotenv()
    db_file = os.getenv('PYHURL_SQLITE_DB', 'db.sqlite3')

    @classmethod
    def __get_connection(cls):
        try:
            return sqlite3.connect(cls.db_file)
        except sqlite3.OperationalError:
            parent_folder = os.path.dirname(cls.db_file)
            if not os.path.exists(parent_folder):
                os.makedirs(parent_folder)
            return sqlite3.connect(cls.db_file)

    @classmethod
    def execute_script(cls, script):
        connection = cls.__get_connection()
        connection.executescript(script)
        connection.commit()
        connection.close()

    @classmethod
    def execute_query(cls, sql, sql_params=None):
        connection = cls.__get_connection()
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        if sql_params:
            rows = cursor.execute(sql, sql_params).fetchall()
        else:
            rows = cursor.execute(sql).fetchall()
        connection.close()
        return rows

    @classmethod
    def execute_update(cls, sql, params=None) -> Optional[int]:
        connection = cls.__get_connection()
        cursor = connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        last_id = cursor.lastrowid
        connection.commit()
        connection.close()
        return last_id
