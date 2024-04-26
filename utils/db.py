import mysql.connector

from utils.init import config


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

    def exec(self, sql, param):
        if not self.conn.is_connected():
            self.conn.reconnect()
        cursor = self.conn.cursor()
        cursor.execute(sql, param)
        cursor.close()
        self.conn.close()
    def query(self, sql,param):
        if not self.conn.is_connected():
            self.conn.reconnect()
        cursor = self.conn.cursor()
        cursor.execute(sql,param)
        result = cursor.fetchall()
        cursor.close()
        self.conn.close()
        return result

    def delete(self, sql,param):
        if not self.conn.is_connected():
            self.conn.reconnect()
        cursor = self.conn.cursor()
        cursor.execute(sql,param)
        result = cursor.fetchall()
        cursor.close()
        self.conn.close()

    def insert_batch(self, sql, param):
        if not self.conn.is_connected():
            self.conn.reconnect()
        cursor = self.conn.cursor()
        cursor.executemany(sql, param)
        cursor.close()
        self.conn.close()

    def insert(self, sql, param):
        if not self.conn.is_connected():
            self.conn.reconnect()
        cursor = self.conn.cursor()
        cursor.execute(sql, param)
        cursor.close()
        self.conn.close()

    def getWeekDateAreaByCurrent(self, date_str) -> list:
        if not self.conn.is_connected():
            self.conn.reconnect()
        from utils.common import currentDateYYYYMMDD
        if date_str is None or len(date_str) == 0:
            date_str = currentDateYYYYMMDD()
        sql = f"""
            SELECT
                DATE_FORMAT(start_date, '%Y-%m-%d') AS start_of_week,
                DATE_FORMAT(end_date, '%Y-%m-%d') AS end_of_week
            FROM (
                SELECT
                    DATE_ADD(STR_TO_DATE(CONCAT('2024', ' ', '1', ' ', '1'), '%X %V %w'), INTERVAL ((WEEK('{date_str}') - 1) * 7) DAY) AS start_date,
                    DATE_ADD(STR_TO_DATE(CONCAT('2024', ' ', '1', ' ', '1'), '%X %V %w'), INTERVAL ((WEEK('{date_str}') - 1) * 7 + 6) DAY) AS end_date
            ) AS week_16;
            """
        rows = self.query(sql,None)
        result = [rows[0][0], rows[0][1]]
        return result

    def getLastWeekDateAreaByCurrent(self, date_str) -> list:
        if not self.conn.is_connected():
            self.conn.reconnect()
        from utils.common import currentDateYYYYMMDD
        if date_str is None or len(date_str) == 0:
            date_str = currentDateYYYYMMDD()
        sql = f"""
             SELECT
                 DATE_FORMAT(start_date, '%Y-%m-%d') AS start_of_week,
                 DATE_FORMAT(end_date, '%Y-%m-%d') AS end_of_week
             FROM (
                 SELECT
                     DATE_ADD(STR_TO_DATE(CONCAT('2024', ' ', '1', ' ', '1'), '%X %V %w'), INTERVAL ((WEEK('{date_str}') - 2) * 7) DAY) AS start_date,
                     DATE_ADD(STR_TO_DATE(CONCAT('2024', ' ', '1', ' ', '1'), '%X %V %w'), INTERVAL ((WEEK('{date_str}') - 2) * 7 + 6) DAY) AS end_date
             ) AS week_16;
             """
        rows = self.query(sql, None)
        result = [rows[0][0], rows[0][1]]
        return result

    def close(self):
        self.conn.close()
