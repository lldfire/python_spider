# -*- coding: utf-8 -*-
import scrapy, json, re, time
from wandou.items import WandouItem
from urllib.parse import urlencode  #将ajax请求参数拼接为完整url
from lxml import etree


class GetCateSpider(scrapy.Spider):
    name = 'get_cate'
    allowed_domains = ['www.wandoujia.com']
    start_urls = ['https://www.wandoujia.com/category/app']
    ajax_url = 'https://www.wandoujia.com/wdjweb/api/category/more?'

    def parse(self, response):
        #解析分类url的标签 li
        urllist = response.selector.xpath('//li[@class="parent-cate"]')
        print(urllist)
        
        #解析一级分类的url
        for v in urllist:
            item = WandouItem()
            #item['cate_name'] = v.xpath('.//a/@title').extract_first()

            item['cate_url'] = v.xpath('.//a/@href').extract_first()
            item['cate_id'] = item['cate_url'].split('/').pop()
            #print(item)

            #请求分类详情页
            for page in range(1,6):
                #首页直接请求
                if page == 1:
                    yield scrapy.Request(url = item['cate_url'], callback = self.parse_info) #首页
                #其他页面需要使用ajax_url请求
                else:
                    #ajax请求参数
                    params = {
                        'catId':item['cate_id'],
                        'ctoken':'zmpcoqlEKVpXd9ONJH59i8No',
                        'page':page,
                        'subCatId':'0',
                    }
                    ajax_url = self.ajax_url + urlencode(params)
                    #print(ajax_url)
                    yield scrapy.Request(url = ajax_url, callback = self.parse_json)
                time.sleep(2)

          
            time.sleep(10)

            

        #访问一级分类的url爬取app的url
    #解析首页
    def parse_info(self, response):
        #解析首页当中的app  的li标签
        appurl_list = response.selector.xpath('.//ul[@id="j-tag-list"]//li')
        for  v in appurl_list:
            item = WandouItem()
            item['app_name'] = v.xpath('.//div[2]/h2/a/text()').extract_first()
            item['app_url'] = v.xpath('.//div[1]//a/@href').extract_first()

            #print(item)

            yield item

    #解析首页之外的页码
    def parse_json(self, response):
        #将相应结果转化为json格式，以便提取数据 
        data = json.loads(response.text)
        html_str = data['data']['content']

        #使用正则解析出所有的li标签
        #pat = '(<li .*? </li>)'
        appurl_list = re.findall('(<li .*? </li>)', html_str, re.S)
        #print(len(appurl_list))
        for item in appurl_list:
            v = etree.HTML(item)
            item = WandouItem()
            item['app_name'] = v.xpath('.//div[2]/h2/a/text()')[0]
            item['app_url'] = v.xpath('.//div[1]//a/@href')[0]

            #print(item)

            yield item