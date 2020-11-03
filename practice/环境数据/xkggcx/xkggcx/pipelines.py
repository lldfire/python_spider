# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import time
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR, DATETIME


class XkggcxPipeline:
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    def __init__(self, host, port, user, pwd, db, table_name):
        # 初始化变量
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db
        self.table_name = table_name

    @classmethod  # 使用装饰器调用类的静态方法
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings['MYSQL_HOST'],
            user=crawler.settings['MYSQL_USER'],
            pwd=crawler.settings['MYSQL_PWD'],
            db=crawler.settings['MYSQL_DB'],
            port=crawler.settings['MYSQL_PORT'],
            table_name=crawler.settings['TABLE_NAME']
        )

    def open_spider(self, spider):
        self.engine = create_engine(
            f'mysql+pymysql://{self.user}:{self.pwd}@{self.host}/{self.db}?charset=UTF8MB4'
        )
    
    # def insert(self, data, table_name: str, lt=False) -> None:
    def process_item(self, item, spider):
        """
        将数据写入数据库中
        """
        data = dict(item)
        # 指定建表时的数据类型
        type_dict = {key: VARCHAR(length=255) for key in data}
        df = pd.DataFrame([data])

        df['inserttime'] = time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.localtime())
        # 指定插入时间的格式为时间格式
        type_dict['inserttime'] = DATETIME()
        # print(df)
        df.to_sql(
            self.table_name,
            self.engine,
            index=False,
            if_exists='append',
            dtype=type_dict
        )
        return item

    def close_spider(self, spider):
        self.engine.dispose()
