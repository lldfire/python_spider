# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HuyaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    room_url = scrapy.Field()     #直播地址
    room_title = scrapy.Field()   #房间名
    room_number = scrapy.Field()  #房间号
    host_name = scrapy.Field()    #主播名
    host_type = scrapy.Field()    #类型
    game = scrapy.Field()    #游戏名
    live_count = scrapy.Field()   #在线人数
    subscribe = scrapy.Field()    #订阅数
    #proxy = scrapy.Field()   #代理ip

    #start_time = scrapy.Field()
    #offset  = scrapy.Field()