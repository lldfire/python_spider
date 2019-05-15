# -*- coding: utf-8 -*-
import scrapy
import json
from huya.items import HuyaItem
from urllib.parse import urlencode
# 此法只能获取第一页的房间信息，无法获取其于页
# 先如此，日后再想办法完善


class LolSpider(scrapy.Spider):
    name = 'lol'
    allowed_domains = ['www.huya.com']
    #start_urls = ['https://www.huya.com/g/lol']
    first_url = 'https://www.huya.com/g/lol'
    axjx_url = 'https://www.huya.com/cache.php?'
    room_url = 'http://www.huya.com/'

    def start_requests(self):
        """创建请求方法，访问所有子页面中的房间"""
        last_page = 37  # 共37页数据，先获取前2页
        #first_url = 'https://www.huya.com/g/lol'
        for i in range(1, last_page+1):
            if i == 1:
                yield scrapy.Request(url=self.first_url, callback=self.parse)
                # time.sleep(random.randint(3,6))

            else:
                data = {
                    'do': 'getLiveListByPage',
                    'gameId ': '1',
                    'm': 'LiveList',
                    'page': i,
                    'tagAll': '0',
                }
                axjx_url = self.axjx_url + urlencode(data)
                # print(axjx_url)
                yield scrapy.Request(url=axjx_url, callback=self.parse)
                # time.sleep(random.randint(3,6))

    def parse(self, response):
        """解析获取房间url,分2步，第一步获取首页，第二步获取ajax页"""
        # 获取信息列表
        # 进行判断如果是第一页则使用一下方法解析，否则解析json格式的
        if response.url == 'https://www.huya.com/g/lol':
            # 解析第一页内容
            room_url_lists = response.selector.xpath(
                './/ul[@id="js-live-list"]//li')
            # print(room_url_lists)
            for v in room_url_lists:
                # print(v)
                room_url = v.xpath('//a[2]/@href').extract_first()
                # print(room_url)

                # 请求房间链接,调用解析网页的函数
                yield scrapy.Request(url=room_url, callback=self.parse_page)
                # break

        # 解析axjx页,获取房间号,拼接房间url http://www.huya.com/12910838
        else:
            # 响应结果编码
            # print(response.url)
            res = json.loads(response.body)
            data = res.get('data')
            room_id_lists = data.get('datas')  # 取出房间id列表
            # print(len(room_id_lists))
            for v in room_id_lists:
                room_id = v['profileRoom']  # 获取房间id
                # print(room_id)
                room_url = self.room_url + str(room_id)

                # 访问房间号
                yield scrapy.Request(url=room_url, callback=self.parse_page)

                # break

    def parse_page(self, response):
        '''解析房间详情信息'''
        item = HuyaItem()
        item['room_url'] = response.url
        item['room_title'] = response.xpath(
            './/h1[@id="J_roomTitle"]/text()').extract_first()
        item['room_number'] = response.xpath(
            './/span[@class="host-rid"]/em/text()').extract_first()
        item['host_name'] = response.xpath(
            './/h3[@class="host-name"]/text()').extract_first()
        item['host_type'] = response.xpath(
            './/span[@class="host-channel"]//a[1]/text()').extract_first()
        item['game'] = response.xpath(
            './/span[@class="host-channel"]//a[2]/h3/text()').extract_first()
        item['live_count'] = int(response.xpath(
            './/span[@class="host-spectator"]//em/text()').extract_first().replace(',', ''))
        item['subscribe'] = int(response.xpath(
            './/div[@id="activityCount"]/text()').extract_first())
        # print(item)
        yield item
