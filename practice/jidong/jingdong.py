# 效率太低

from xiciproxy import daili  # 导入代理类，
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import time
import csv
import os
from selenium.common.exceptions import TimeoutException
from lxml import etree
import pandas as pd


# 搜索目标
kw = '笔记本电脑'
maxpage = 30


def open_firefox():
    """#获取代理"""
    proxies = daili()  # 创建对象获取代理ip
    my_proxy = proxies.get_ip()
    print('当前代理：', my_proxy)
    # print(type(int(my_proxy.split(':')[1])))
    #selenium +firefox设置代理,并创建请求对象
    profile = webdriver.FirefoxOptions()
    profile.add_argument('-headless')  # 设置无界面模式
    # 设置代理服务器
    profile.set_preference('network.proxy.type', 1)  # 代理类型（http,https）为0时不发送
    profile.set_preference('network.proxy.http', my_proxy.split(':')[
                           0])  # IP为你的代理服务器地址:如‘127.0.0.0’，字符串类型
    profile.set_preference('network.proxy.http_port', int(
        my_proxy.split(':')[1]))  # PORT为代理服务器端口号:如，9999，int类型
    browser = webdriver.Firefox(options=profile)
    # browser.get('http://httpbin.org/get')
    # print(browser.page_source)
    # browser.close()
    return browser


def save_products(info):
    """保存文件信息"""
    file_size = os.path.getsize(r'.\computers.csv')  # 获取路径文件的大小
    if file_size == 0:
        # 表头
        name = ['comuter_id', 'computer_name', 'computer_price',
                'computer_commit', 'info_url', 'img_url']

        file_test = pd.DataFrame(columns=name, data=info)
        file_test.to_csv(r'.\computers.csv', encoding='utf-8', index=False)
    else:
        with open(r'.\computers.csv', 'a+', newline='') as file_test:
            writer = csv.writer(file_test)
            writer.writerows(info)  # 写入多行，单行writerow(info)


def get_products(browser):
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    # print(soup.title.string)
    result = soup.find_all(attrs={'id': 'J_goodsList'})
    items = result[0].find_all(name='li')
    print('商品总量：', len(items))

    # 遍历商品列表中的信息，以lxml提取数据
    products_list = []  # 存储多个商品信息

    for item in items:

        each = etree.HTML(str(item))
        # print(each)
        image_url = each.xpath('//div[@class="p-img"]/a/img/@src')
        if len(image_url) == 0:
            image_url = None
        else:
            image_url = image_url[0]
            #image_url = image_url.replace()

        info_url = each.xpath('//div[@class="p-img"]/a/@href')[0]
        #info_url = info_url.replace()

        price = each.xpath('//div[@class="p-price"]/strong/i/text()')[0]

        # c此标签的class属性为多个，需要用contains(@属性,'属性值')  包含即可
        name = each.xpath('//div[contains(@class, "p-name")]/a/em/text()')[0]
        commit = each.xpath('//div[@class="p-commit"]/strong/a/text()')[0]
        product_id = each.xpath('//div[@class="p-icons"]/@id')[0]

        # print(name)

        # 存储单个商品属性
        product_list = [product_id, name, price, commit, info_url, image_url]
        products_list.append(product_list)
    print(len(products_list))
    # break
    #print('正在保存第%d页数据' % ((int(p)+1)/2))
    save_products(products_list)


def get_page():
    for p in range(1, maxpage*2 + 1, 2):  # 遍历所有数据
        browser = open_firefox()

        print('正在获取并保存第%d页数据' % ((int(p)+1)/2))
        req_url = 'https://search.jd.com/Search?keyword={}&enc=utf-8&page={}'.format(
            kw, p)
        try:
            browser.get(req_url)
            # 等待网页中关键内容加载，WebDriverWait
            time.sleep(1)

            # print(browser.page_source)
        except TimeoutException as TE:
            print('The reason is:', TE)

        get_products(browser)

        browser.close()

        # get_products()  #每爬取一次，就执行一次获取商品信息的函数
        # break #测试时只获取第一页代码


if __name__ == '__main__':
    get_page()
    # get_products()
    # browser.close()
