# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WandouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'appurl'  #保存app_url的集合

    cate_name = scrapy.Field()  #分类名
    cate_url = scrapy.Field()  #分类url
    cate_id = scrapy.Field()  #分类id
    app_name = scrapy.Field()  #app名
    app_url = scrapy.Field()  #app url
    app_size = scrapy.Field()  #app体积
    app_content = scrapy.Field()  #评论数
    app_count = scrapy.Field()  #app下载数

