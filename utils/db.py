import mysql.connector

from utils.common import config


class MySQLClient:
    def __init__(self, name):
        self.conn = mysql.connector.connect(
            host=config[name]['mysql']['host'],
            user=config[name]['mysql']['username'],
            password=config[name]['mysql']['password'],
            database=config[name]['mysql']['database'],
            autocommit=True,
            charset="utf8mb4"
        )

    def query(self, sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def insert_batch(self, sql, param):
        cursor = self.conn.cursor()
        cursor.executemany(sql, param)
        cursor.close()

    def insert(self, sql, param):
        cursor = self.conn.cursor()
        cursor.execute(sql, param)
        cursor.close()

    def close(self):
        self.conn.close()
