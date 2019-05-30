#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-05-14 16:11:37
# @Author  : lldpy (1723031704@qq.com)
# @Link    : https://github.com/lldfire/
# @Version : $Id.1$

# mysql数据库快捷连接的类，数据库相关配置在setting中配置
import os
import configparser
import pymysql

# 改变当前工作目录到指定目录
os.chdir(r'C:\Users\86132\mysql_con')
cf = configparser.ConfigParser()

# 从配置文件中读取数据库连接参数
cf.read(r'setting.conf')
host = cf.get('db', 'HOST')
port = cf.get('db', 'PORT')
user = cf.get('db', 'USER')
db = cf.get('db', 'DB')
pswd = cf.get('db', 'PASSWORD')


class ConnectMysql:
    """
    工作中常用的封装，包括数据的存储和预处理类
    """

    def __init__(self):
        self.host = host
        self.user = user
        self.password = pswd
        self.database = db
        self.port = int(port)

    def connect_mysql(self):
        """
        建立数据库的连接，生成一个游标对象
        """
        self.conn = pymysql.Connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.database,
            charset='utf8',
            port=self.port)
        self.cursor = self.conn.cursor()

    def batch_insert(self, table, data):
        """
        新增数据，数据格式为dict
        table: 表名
        data : 数据，标准字典格式，key必须与数据库中的字段保持一致
        """
        assert type(table) == str, '表名必须为字符串'
        assert type(data) == dict, '数据类型必须为"dict"'

        keys = ','.join(data.keys())
        values = ','.join(['%s']*len(data))
        sql = 'insert into %s(%s) values(%s)' % (table, keys, values)

        self.conn.ping(reconnect=True)   # 检查数据库是否连接，
        try:
            self.cursor.execute(sql, tuple(data.values()))
            self.conn.commit()  # 提交事务
        except pymysql.err.IntegrityError as er:
            print('数据重复:\n', er)
        except pymysql.err.InternalError as er:
            raise Exception('数据表错误:\n', er)
        except pymysql.err.DataError as er:
            raise Exception('数据存在错误:\n', er)

    def exe_query(self, sql):
        """
        执行查询语句
        : return 2D tuple
        """
        try:
            self.cursor.execute(sql)
        except Exception as er:
            print('查询失败，失败原因：\n', er)
        else:
            return self.cursor.fetchall()

    def exe_not_query(self, sql):
        """
        执行非查询语句
        """
        self.cursor.execute(sql)
        self.conn.commit()

    def close_connect(self):
        """
        关闭游标对象，断开数据库连接
        """
        self.cursor.close()
        self.conn.close()
        print('数据库已关闭！')

    def save_file(self, pathname, data, lock):
        """
        文件存储模块
            pathname: 文件写入的路径和文件名
            data: str object 待写入的数据
        return: None
        """
        lock.acquire()
        with open(pathname, 'a+', encoding='utf-8') as file:
            file.write(data + '\n')
        lock.release()
        return None

    def read_file(self, path, delete=False):
        """
        文件读取,仅读取和读取后删除两种模式
            path: 待读取文件的路径
            rewrite: Boolean Object, Ture-读取并删除内容，False-仅读取
        return: list
        """
        with open(path, 'r', encoding='utf-8') as f:
            url_list = f.readlines()
        if delete:
            os.remove(path)
        return [i.replace('\n', '') for i in url_list]

    def clear_data(self, data: dict):
        """
        数据处理，清除字典中的特殊符，如英文单双引号、制表、换行、转义等，
        主要用于xpath提取后的数据处理
            data: dict Object
        return: dict
        """
        if isinstance(data, dict):
            for k, v in data.items():
                # 判断values的类型，如果是dict则递归调用其本身
                if isinstance(v, list):
                    data[k] = v[0].strip().replace(
                        '\\', '/').replace("\r", '').replace(
                        '\n', '').replace('\t', '').replace(
                        '"', '”').replace("'", '‘').replace(
                        "  ", '').replace('&nbsp', '') if v else ''

                if isinstance(v, str):
                    data[k] = v.strip().replace(
                        '\\', '/').replace("\r", '').replace(
                        '\n', '').replace('\t', '').replace(
                        '"', '”').replace("'", '‘').replace(
                        "  ", '').replace('&nbsp', '') if v else ''
                if isinstance(v, dict):
                    self.clear_data(v)
            return data
