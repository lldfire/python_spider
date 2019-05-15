#多进程 + 多线程
import requests
from lxml import etree
import time
import os
import re
import random
from fake_useragent import UserAgent
from multiprocessing import Pool
from threading import Thread


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    # 'Cookie':'__cfduid=dabe3f1f6d7a2bf87dc10…OYnZeCC_rJs1U8l5ARL1r1a2_pCVef',
    'Host': 'www.doutula.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent ': '',
}

# 多进程抓取图片链接


def get_one_page(page_url):
    """抓取所有的url，并存储"""
    # url = 'http://www.doutula.com/photo/list/?page=%s' % page
    # 伪装浏览器
    try:
        ua = UserAgent()
        headers['User-Agent'] = ua.random
        response = requests.get(page_url, headers=headers)

        # 解析网页，获取url
        html = etree.HTML(response.content.decode('utf-8'))
        # print(html)
        return html
    except:
        print('请求失败！')


def get_many_page(url_list: list):

    for url in url_list:
        try:
            html = get_one_page(url)
        except:
            continue
        # time.sleep(0.4)
        return html


def get_all_pageurl(start_page, max_page):
    """生成所有页面的url链接"""
    page_url_list = []

    for page in range(start_page, max_page+1):
        try:

            page_url = 'http://www.doutula.com/photo/list/?page=%s' % page
            page_url_list.append(page_url)
        except:
            continue
    return page_url_list


def parse(html):
    """解析网页内容，获取表情包链接"""
    # 一页有68个表情，
    img_list = []

    for i in range(1, 69):
        try:
            img_label = html.xpath(
                '//*[@id="pic-detail"]/div/div[3]/div[2]/ul/li/div/div/a[%s]//img' % i)
            # 判断img标签的长度 //*[@id="pic-detail"]/div/div[3]/div[2]/ul/li/div/div/a[68]/img[2]
            # print(len(img_label))
            if len(img_label) == 1:
                img_url = html.xpath(
                    '//*[@id="pic-detail"]/div/div[3]/div[2]/ul/li/div/div/a[%s]/img/@data-original' % i)[0]
                img_list.append(img_url)

            # 动图 //*[@id="pic-detail"]/div/div[3]/div[2]/ul/li/div/div/a[61]/img[2]
            if len(img_label) == 2:
                img_url = html.xpath(
                    '//*[@id="pic-detail"]/div/div[3]/div[2]/ul/li/div/div/a[%s]//img[2]/@data-original' % i)[0]
                img_list.append(img_url)
        except:
            continue

    return img_list


def download_one_img(url):
    """保存单张图片"""
    # 设置保存文件名
    try:
        img_name = str(int(time.time() * 1000) + random.randint(1, 100000))
        file_name = '.'.join([img_name, 'jpg'])
        path = r'C:\Users\13772\Desktop\python\myspider\actual\doutu\biaoqing'
        all_path = os.path.join(path, file_name)

        # 设置浏览器代理
        ua = UserAgent()
        img_headers = {
            'User-Agent': ua.random,
        }

        # 将请求结果写入
        response = requests.get(url, headers=img_headers)
        # print(response.content)
        # try:
        with open(all_path, 'ab') as file:
            file.write(response.content)
    except:
        print('出问题了')


def download_more_img(url_list: list):
    """下载所有每页中的所有图片"""

    for url in url_list:
        try:
            download_one_img(url)
        except:
            continue
            print('下载失败')


def allot_page(page_url: list, n=4):
    """将页面url列表分组"""
    size = len(page_url)
    base = int(size/4)  # 每组基础url数量
    remainder = size % 4
    page_groups = [page_url[(i * base): ((i + 1) * base)]
                   for i in range(n)]  # 切片为4个分组
    # 剩余未被分组的url取出来
    remainder_list = page_url[n*base:]
    # 将剩余url依次添加至分组中
    for i in range(remainder):
        page_groups[i].append(remainder_list[i])

    return [i for i in page_groups]  # 返回一个二维列表


def allot_img_url(img_url: list, n=4):
    """将解析出来的图片链接列表分组，方法同上"""
    size = len(img_url)
    base = int(size/4)  # 每组基础url数量
    remainder = size % 4
    img_groups = [img_url[(i * base): ((i + 1) * base)]
                  for i in range(n)]  # 切片为4个分组
    # 剩余未被分组的url取出来
    remainder_list = img_url[n*base:]
    # 将剩余url依次添加至分组中
    for i in range(remainder):
        img_groups[i].append(remainder_list[i])

    return [i for i in img_groups]


# 多进程爬取3-100页
def multiprocess_spider_img(page_url_list: list, processes=4):
    """多进程下载表情"""
    pool = Pool(processes)
    for page_url in page_url_list:
        print('正在保存：%s' % page_url)
        html = get_one_page(page_url)
        img_list = parse(html)
        groups = allot_img_url(img_list, n=processes)

        # 多进程请求页面
        for group in groups:
            pool.apply_async(func=download_more_img, args=(group,))
    pool.close()
    pool.join()


# 多线程
def multithread_spider_img(url_list: list, threads: int = 60):
    """多线程下载表情"""
    begin = 0
    while True:
        thread_list = []
        urls = url_list[begin: begin + threads]  # 取出与线程数相当的url

        if not urls:
            break

        for u in urls:
            t = Thread(target=download_one_img, args=(u,))
            thread_list.append(t)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for t in thread_list:
            t.join()

        begin += threads

# 使用多进程请求并解析页面，将解析结果使用一个列表接收，再使用多线程下载


def run_parse(page_url_list: list, processes: int = 4):
    """运行解析函数，获取表情url"""
    pass


def main():
    start = time.time()
    #url_list = parse(get_one_page(5))
    #url = 'http://img.doutula.com/production/uploads/image//2019/01/21/20190121037113_oeQSwZ.gif!dta'
    # download_one_img(url)
    # download_more_img(url_list)

    page_url_list = get_all_pageurl(201, 210)

    for page_url in page_url_list:
        try:
            print('正在保存：%s' % page_url)
            html = get_one_page(page_url)
            img_list = parse(html)
            # 同步爬虫  10页 83.71
            # download_more_img(img_list)

            # 多线程  35线程 16秒，70线程
            multithread_spider_img(img_list, 70)

        except:
            continue

    # 多进程  10页  17.95秒
    #page_url_list = get_all_pageurl(88,100)
    #multiprocess_spider(page_url_list, 4)

    end = time.time()
    print('耗时%.2f秒' % (end - start))


if __name__ == '__main__':
    main()
