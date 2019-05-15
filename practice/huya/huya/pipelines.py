# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class HuyaPipeline(object):
    def process_item(self, item, spider):
        print(item)


class Mysqlpipline(object):
    def __init__(self, host, port, user, pwd, db):
        # 初始化变量
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db

    @classmethod  # 使用装饰器调用类的静态方法
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            user=crawler.settings.get('MYSQL_USER'),
            pwd=crawler.settings.get('MYSQL_PWD'),
            db=crawler.settings.get('MYSQL_DB'),
            port=crawler.settings.get('MYSQL_PORT')
        )

    def open_spider(self, spider):
        """建立数据库连接,创建游标对象"""
        self.db = pymysql.connect(host=self.host, port=self.port,
                                  user=self.user, password=self.pwd, db=self.db, charset='utf8')
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        # sql语句
        sql = 'insert into allhost(room_num, room_url, room_title, host_name, host_type, game, live_count, subscribe)\
            values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (item['room_number'], item['room_url'],
                                                                       item['room_title'], item['host_name'], item['host_type'], item['game'], item['live_count'], item['subscribe'])

        self.cursor.execute(sql)  # 执行sql语句

        self.db.commit()  # 事务提交

    def close_spider(self, spider):
        self.db.close()
