# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XkggcxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    省市 = scrapy.Field()
    地市 = scrapy.Field()
    许可证编号 = scrapy.Field()
    单位名称 = scrapy.Field()
    行业类别 = scrapy.Field()
    撤销原因 = scrapy.Field()
    撤销时间 = scrapy.Field()
