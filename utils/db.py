import logging

import mysql.connector
from mysql.connector import pooling

from utils.init import config


class MySQLClient:
    def __init__(self, name):
        pool_config = {
            'pool_name': 'pocs',
            'pool_size': 5,  # 连接池大小
            'pool_reset_session': True,  # 每次从池中获取连接时重置会话状态
            'host': config[name]['mysql']['host'],
            # 'port': config_data['mysql']['port'],
            'database': config[name]['mysql']['database'],
            'user': config[name]['mysql']['username'],
            'password': config[name]['mysql']['password'],
        }
        try:
            self.conn = pooling.MySQLConnectionPool(**pool_config)
        except mysql.connector.Error as err:
            logging.error(f"Error connecting to MySQL: {err}")

    def exec(self, sql, param):
        conn = self.conn.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, param)
        conn.commit()
        cursor.close()
        conn.close()

    def query(self, sql, param):
        conn = self.conn.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, param)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def delete(self, sql, param):
        conn = self.conn.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, param)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()

    def insert_batch(self, sql, param):
        conn = self.conn.get_connection()
        cursor = conn.cursor()
        try:
            for i in range(0, len(param), 5000):
                batch = param[i:i + 5000]
                cursor.executemany(sql, batch)
                # 提交当前批次的更改
                conn.commit()
            # cursor.executemany(sql, param)
        except Exception as e:
            print(e)
        cursor.close()
        conn.close()

    def insert(self, sql, param):
        conn = self.conn.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, param)
            conn.commit()
        except Exception as e:
            print(e)
        cursor.close()
        conn.close()

    def getWeekDateAreaByCurrent(self, date_str) -> list:
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
        rows = self.query(sql, None)
        result = [rows[0][0], rows[0][1]]
        return result

    def getLastWeekDateAreaByCurrent(self, date_str) -> list:
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
        conn = self.conn.get_connection()
        conn.close()
