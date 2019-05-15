import requests
import time
from bs4 import BeautifulSoup
from lxml import etree
from random import randint
#import pandas as pd
import xlrd
import re
import os
import csv
from fake_useragent import UserAgent  # 导入随机浏览器模块


# 读取url存入列表中

def get_urls():
    info_urls = []
    with open('./info_urls.txt', 'r') as urlfile:
        lines = urlfile.readlines()
        # 判断url格式是否正确

        for j in range(len(lines)):
            info_urls.append(lines[j].split('?')[0])
            # print(info_urls)
            # break
        print('总共%s条url' % (j+1))

    return info_urls

# 请求url


def get_page(url):
    ua = UserAgent()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '__trackId=154479343522408; __city=shanghai; Hm_lvt_5a727f1b4acc5725516637e03b07d3d2=1544793438,1545054371,1545131623; _ga=GA1.2.702845611.1544793440; __admx_track_id=LZJJ8nXyb8dGD19P7DBQwQ; __admx_track_id.sig=5rKQhpA5LltS2mAIGqzRsQ3Yh9k; _gid=GA1.2.465819993.1545054373; Hm_lpvt_5a727f1b4acc5725516637e03b07d3d2=1545141808; __s=clg9vjjcm53s1bvmjo5o4ie141; __sense_session_pv=4; _gat=1',
        'Host': 'shanghai.baixing.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': ua.random,
    }
    try:
        res = requests.get(url, headers=headers)
        print('状态码：', res.status_code)
        if res.status_code == 200:
            return res.text
        else:
            return None
    except:
        return None


# 解析网页
def parse_page(html):
    try:
        # 获取联系方式
        soup = BeautifulSoup(html, 'lxml')  #
        mobile = etree.HTML(str(soup.find_all(id='mobileNumber')[0]))  # 定位电话号码
        phone = mobile.xpath('.//strong/text()')[0]

        # 获取简要信息
        main_info = etree.HTML(
            str(soup.find_all(attrs={'class': 'viewad-topMeta'})[0]))

        price = main_info.xpath('.//ul/li[1]/span/text()')[0]
        deposit = main_info.xpath('.//ul/li[2]/span/text()')[0]
        #address = main_info.xpath('.//ul/li[4]/span//span[2]/text()')[0]

        # 判断是否获取到小区名称
        village = main_info.xpath('.//ul/li[3]/span/a/text()')
        if len(village) == 1:
            village_name = village[0]
        else:
            village_name = main_info.xpath('.//ul/li[3]/span/text()')[0]

        # h获取其他信息
        other_info = etree.HTML(
            str(soup.find_all(attrs={'class': 'viewad-detail'})[0]))

        rent_method = other_info.xpath('.//div[2]//div[2]/a/text()')[0]
        region = other_info.xpath('.//div[2]//div[3]//label[2]/text()')[0]
        harea = other_info.xpath('.//div[2]//div[4]//label[2]/text()')[0]
        floors = other_info.xpath('.//div[2]//div[5]//label[2]/text()')[0]
        orientation = other_info.xpath('.//div[2]//div[6]//label[2]/text()')[0]
        address = other_info.xpath('.//div[2]//div[8]//label[2]/text()')[0]

        info = [village_name, phone, address, price, rent_method,
                deposit, region, harea, floors, orientation]
        # print(info)
        return info
    # return deposit,address,village_name,phone,price,rent_method,region,harea,floors,orientation

    except:
        print('未解析到内容')
        return None


# 存储至xlsx文件中
def save_info(info):
    file_size = os.path.getsize(r'.\infos.csv')  # 获取目标文件大小
    # print(file_size)

    if file_size == 0:
        # 表头
        name = ['小区', '电话', '地址', '价格', '租赁方式', '押金', '装修', '面积', '楼层', '朝向']
        '''
        #建立DataFrame对象
        file_test = pd.DataFrame(columns = name, data = info) #DataFrame中有两个参数，均是列表
        file_test.to_csv(r'.\infos.csv', encoding='gbk', index=False) #使用to_csv方法将数据写入
        '''
        #data = [name,info]
        with open(r'.\infos.csv', 'a+', newline='') as file_test:
            # 初始化写入文件，传入句柄，调用 writerows方法
            writer = csv.writer(file_test)
            writer.writerow(name)
            writer.writerow(info)
    else:  # 不需要创建表头
        with open(r'.\infos.csv', 'a+', newline='') as file_test:
            # 初始化写入文件，传入句柄，调用 writerows方法
            writer = csv.writer(file_test)
            writer.writerow(info)  # writerow 单行写入，writerows多行写入，列表为二维列表

# 主函数


def main():

    info_urls = get_urls()
    # print(info_urls) #当前 url

    i = 0
    for url in info_urls:
        print(url)
        html = get_page(url)
        if html:
            info = parse_page(html)
            if info:
                save_info(info)
        i += 1
        print('正在请求第%d条' % i)
        if i % 5 == 0:
            sleep = randint(6, 14)
            print('休息{}秒'.format(sleep))
            time.sleep(sleep)
        if i % 100 == 0:
            print('暂停30秒')
            time.sleep(30)

    '''
    url = 'http://shanghai.baixing.com/zhengzu/a1634880724.html?from=suggestion&sgs=stepback'
    html = get_page(url)
    if html:
        info = parse_page(html)
        print(info)
    '''


if __name__ == '__main__':
    main()
