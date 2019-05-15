# -*- coding: utf-8 -*-
import scrapy
import pymongo
import time, re 
from wandou.items import WandouItem


class GetInfoSpider(scrapy.Spider):
    name = 'get_info'
    allowed_domains = ['www.wandoujia.com']
    start_urls = ['https://www.wandoujia.com/']

    def parse(self, response):
        #获取数据库中的数据，遍历所有url 进行访问
        client = pymongo.MongoClient('localhost')
        db = client.wandoujia
        cursor = db.collection.find()
        url_list = [cur['app_url'] for cur in cursor]

        client.close()  #关闭数据库
        i = 0
        for url in url_list:
            print(url)
            yield scrapy.Request(url = url, callback = self.page_parse)
            
            i += 1
            if i ==5:
                time.sleep(4)
                #break
            time.sleep(1)
            #break


    def page_parse(self, response):
        "解析网页信息"
        item = WandouItem()
        item['app_name'] = response.selector.xpath('.//div[@class="app-info"][1]/p/span/text()').extract_first()
        
        #数据清洗,将数据转化为int
        count = response.selector.xpath('.//div[@class="num-list"]//div[1]//span[1]/i/text()').extract_first()
        if "亿" in count:
            item['app_count'] = int(float(re.findall('([0-9]+[.]*[0-9]*)亿', count)[0])*100000000)
        if "万" in count:
            item['app_count'] = int(float(re.findall('([0-9]+[.]*[0-9]*)万', count)[0])*10000)
        if '亿' not in count and '万' not in count:
            item['app_count'] = int(count)
        #print(type(item['app_count']))

        content = response.selector.xpath('.//div[@class="num-list"]//div[1]/a/i/text()').extract_first()
        item['app_content'] = int(content) #将评论数的格式转化为int
        #print((item['app_content']))

        item['app_size'] = response.selector.xpath('.//div[@class="infos"]/dl//dd[1]/text()').extract_first()
        #item['app_name'] = response.selector.xpath('//div[@class="app-info"][1]/p/span/text()').extract_first()

        #print(item)
        yield item
        

