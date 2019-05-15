# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class WandouPipeline(object):
    def process_item(self, item, spider):
        pass

class MongodbPipline(object):
    """对抓取结果item中的appurl和appname进行存储"""

    #初始化对象
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod  
    def from_crawler(cls, crawler):
        """通过依赖注入方式实例化当前类，并返回，参数是从配置文件获取MongoDB信息"""
        return cls(mongo_url = crawler.settings.get('MONGO_URL'), mongo_db = crawler.settings.get('MONGO_DB'))

    def open_spider(self, spider):
        """spider 自动调用此方法，并连接mongodb,选择数据库"""
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

        #保存app信息 

    def process_item(self, item, spider):
        """选择对应集合并写入itme信息"""
        #collection = 'appurl'
        #appinfos = 'appinfos'
        #self.db.collection.insert(dict(item))  #db.集合名称.insert(document)
        #保存app信息 
        self.db.appinfos.insert(dict(item))
        #print(item) 
        return item

    def close_spider(self, spider):
        '''spider 自动调用，负责关闭mongodb'''
        self.client.close()

