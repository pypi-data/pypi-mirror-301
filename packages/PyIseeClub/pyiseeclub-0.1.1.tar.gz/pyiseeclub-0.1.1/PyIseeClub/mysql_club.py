# -*- coding: utf-8 -*-
from pymysql.cursors import DictCursor


class mysql_tools(object):
    def __init__(self, conn):
        self.conn = conn

    def connect(self):
        """
        启动连接
        :return:
        """
        cursor = self.conn.cursor(cursor=DictCursor)
        return self.conn, cursor

    @staticmethod
    def connect_close(conn, cursor):
        """
        关闭连接
        :param conn:
        :param cursor:
        :return:
        """
        cursor.close()
        conn.close()

    def fetch_all(self, sql, *args):
        """
        批量查询
        :param sql:
        :param args:[]
        :return:
        """
        conn, cursor = self.connect()
        try:
            cursor.execute(sql, args)
            record_list = cursor.fetchall()
        finally:
            self.connect_close(conn, cursor)

        return record_list

    def fetch_one(self, sql, *args):
        """
        查询单条数据
        :param sql:
        :param args:[]
        :return:
        """
        conn, cursor = self.connect()
        try:
            cursor.execute(sql, args)
            result = cursor.fetchone()
        finally:
            self.connect_close(conn, cursor)

        return result

    def insert(self, sql, *args):
        """
        插入数据
        :param sql:
        :param args:[]
        :return:
        """
        conn, cursor = self.connect()
        try:
            row = cursor.execute(sql, args)
            conn.commit()
        finally:
            self.connect_close(conn, cursor)
        return row
