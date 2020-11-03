import datetime
import scrapy
from scrapy import FormRequest
from scrapy.selector import Selector
from xkggcx.items import XkggcxItem


class CxggSpider(scrapy.Spider):
    """ 每天一更 """
    name = 'cxgg'
    allowed_domains = ['permit.mee.gov.cn']
    start_urls = 'http://permit.mee.gov.cn/permitExt/syssb/xkgg/xkgg!xkgg_cxggList.action'
    search_time = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    form = {
        'page.pageNo': '1',
        'page.orderBy': '',
        'page.order': '',
        'province': '',
        'city': '',
        'registerentername': '',
        'treadname': '',
        'treadcode': '',
        'searchTime': '2020-10-30', # search_time
    }

    def start_requests(self):
        yield FormRequest(
            self.start_urls,
            formdata=self.form,
            callback=self.parse_page
        )

    def parse_table(self, selector):
        item = XkggcxItem()
        tr_list = selector.xpath('.//table[@class="tabtd"]/tr')
        for tr in tr_list[1:]:
            item['省市'] = tr.xpath('./td[1]/@title').get()
            item['地市'] = tr.xpath('./td[2]/@title').get()
            item['许可证编号'] = tr.xpath('./td[3]/@title').get()
            item['单位名称'] = tr.xpath('./td[4]/@title').get()
            item['行业类别'] = tr.xpath('./td[5]/@title').get()
            item['撤销原因'] = tr.xpath('./td[6]/@title').get()
            item['撤销时间'] = tr.xpath('./td[7]/@title').get()
            yield item

    def parse_page(self, response):
        selector = Selector(response)
        # 没有解析到页码编码
        # 提取唯一属性标签 class="fr margin-t-33 margin-b-20"
        # 无此标签时，表示无数据

        try:
            pages = selector.xpath('.//div[@class="fr margin-t-33 margin-b-20"]/text()').re('\d+')[0]
        except IndexError:
            pages = -1
        
        if int(pages) == -1:
            pass
        elif int(pages) == 1:
            yield from self.parse_table(selector)
        elif int(pages) > 1:
            yield from self.parse_table(selector)
            for page in range(2, int(pages) + 1):
                self.form['page.pageNo'] = str(page)
                yield FormRequest(
                    self.start_urls,
                    formdata=self.form,
                    callback=self.parse
                )

        else:
            pass
 
    def parse(self, response):
        selector = Selector(response)
        yield from self.parse_table(selector)
