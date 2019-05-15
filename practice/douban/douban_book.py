import requests
import re
import time
from lxml import etree
from fake_useragent import UserAgent
import csv
import os
import pandas as pd
#import pymysql
#import requests.exceptions

#proxy_server = ''
category_url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
host = 'localhost'
port = 3306
user = 'root'
pwd = ''
db = 'mydb'

# ua = UserAgent()
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'Host': 'book.douban.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': '',

}


def error_log(errorInfo):
    errortime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    with open('./crawllog.txt', 'a+') as file:
        file.write('%s : %s /n' % (errortime, str(errorInfo)))


def get_proxy():
    """获取代理ip"""
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "HIBNZ3E65L683RBD"
    proxyPass = "AB1C7E7F19EFB92B"

    #proxy_url = "http://%s:%s@%s:%s" % (proxyUser, proxyPass, proxyHost, proxyPort)
    # 访问服务器

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxy_handler = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    return proxy_handler


def book_category():
    """获取书籍类别"""
    ua = UserAgent()
    headers['User-Agent'] = ua.random
    proxies = get_proxy()
    time.sleep(0.3)  # 代理1秒5个

    response = requests.get(category_url, headers=headers,
                            proxies=proxies, timeout=5)
    if response.status_code == 200:
        html = etree.HTML(response.content.decode('utf-8'))  # 创建xpath能解析的对象
        # 6个class类
        class_list = html.xpath('//*[@id="content"]/div/div[1]/div[2]//div')
        if len(class_list) == 6:
            # 每个class类中有多行
            for items in class_list:
                table_list = items.xpath('./table/tbody//tr')
                # 每行中有多列,遍历
                for item in table_list:
                    cate_list = item.xpath('./td/a/text()')
                    for category in cate_list:
                        # print(category)
                        yield category
    else:
        return None


def maxpage(category):
    """获取最大页码数"""
    ua = UserAgent()
    headers['User-Agent'] = ua.random
    proxies = get_proxy()
    time.sleep(0.3)  # 代理1秒5个

    first_url = 'https://book.douban.com/tag/' + category

    response = requests.get(first_url, headers=headers,
                            proxies=proxies, timeout=5)
    if response.status_code == 200:
        html = etree.HTML(response.content.decode('utf-8'))
        # 获取最后一页页码
        last_page = html.xpath('//*[@id="subject_list"]/div[2]/a[10]/text()')

        # 判断是否有页码，如果没有则最大页码数小于10，有且大于100则设为49
        if last_page:
            max_page = int(last_page[0])
            if max_page >= 50:
                max_page = 49
        else:
            for p in range(9, 3, -1):
                last_page = html.xpath(
                    '//*[@id="subject_list"]/div[2]/a[%d]/text()' % p)
                # 如果取到值就结束循环
                if last_page:
                    max_page = int(last_page[0])
                    break

        return max_page
    else:
        return None


def book_infos(category, page=1):
    """获取分类书籍页面"""
    try:
        ua = UserAgent()
        headers['User-Agent'] = ua.random
        proxies = get_proxy()
        time.sleep(0.3)  # 代理1秒5个
        # print(headers['User-Agent'])

        books_url = 'https://book.douban.com/tag/{}?start={}&type=T'.format(
            category, page*20)
        # 判断访问页面是否请求成功
        response = requests.get(
            books_url, headers=headers, proxies=proxies, timeout=5)
        if response.status_code == 200:
            return response.content.decode('utf-8')
        else:
            return None
    except Exception as e:
        error_log(e)
        return None


def parse(content):
    """解析数据"""
    try:
        html = etree.HTML(content)
        items = html.xpath('//*[@id="subject_list"]/ul//li')
        cate = html.xpath('//*[@id="content"]/h1/text()')[0].split(':')[1]
    except IndexError as IE:
        error_log(IE)
    # 遍历输出
    for item in items:
        # author, translate, book_concern, pub_date, price = '','','','',''
        # assess_count = ''
        try:
            au_tr = item.xpath(
                './/div[@class="info"]//div[1]/text()')[0].replace('\n', '', 5).strip()
            # print(au_tr)
            # 获取作者、翻译、出版社、出版日期、售价信息，如果是中国作者则没有翻译，如果长度不够，则这些信息不输入
            au_tr_list = au_tr.split('/')
            if len(au_tr_list) == 5:
                author = au_tr_list[0]
                translate = au_tr_list[1].strip()
                book_concern = au_tr_list[2].strip()
                pub_date = au_tr_list[3].strip()
                price = au_tr_list[4]

            if len(au_tr_list) == 4:
                author = au_tr_list[0]
                translate = '无'
                book_concern = au_tr_list[1].strip()
                pub_date = au_tr_list[2].strip()
                price = au_tr_list[3]

            if (len(au_tr_list) != 5) and (len(au_tr_list) != 4):
                author = author = au_tr_list[0]
                translate = '无'
                book_concern = '未知'
                pub_date = '未知'
                price = '0.1'

            # 获取评价人数
            assess_count = item.xpath(
                './/div[2]/div[2]/span[3]/text()')[0].replace('\n', '', 2)
            book_infos = {

                'category': cate.strip(),
                'book_name': item.xpath('.//div[2]/h2/a/text()')[0].replace('\n', '', 7).strip(),
                # 'book_id':item.xpath(''),
                'info_url': item.xpath('.//div[1]/a/@href')[0],
                'img_url': item.xpath('.//div[1]/a/img/@src')[0],
                'author': author.strip(),
                'translate': translate,
                'book_concern': book_concern,
                'pub_date': pub_date,
                'assess_count': int(re.findall('([0-9]+)', assess_count)[0]),
                'score': float(item.xpath('.//div[2]/div[2]//span[2]/text()')[0]),
                'price': float(re.findall('([0-9]+\.?[0-9]+)', price)[0]),
            }
        except IndexError as IE:
            error_log(IE)
            try:
                book_infos = {

                    'category': cate.strip(),
                    'book_name': item.xpath('.//div[2]/h2/a/text()')[0].replace('\n', '', 7).strip(),
                    # 'book_id':item.xpath(''),
                    'info_url': item.xpath('.//div[1]/a/@href')[0],
                    'img_url': item.xpath('.//div[1]/a/img/@src')[0],
                    'author': author.strip(),
                    'translate': translate,
                    'book_concern': book_concern,
                    'pub_date': pub_date,
                    'assess_count': 0,
                    'score': 0.0,
                    'price': float(re.findall('([0-9]+\.?[0-9]+)', price)[0]),
                }
            except IndexError:
                try:
                    book_infos = {
                        'category': cate.strip(),
                        'book_name': item.xpath('.//div[2]/h2/a/text()')[0].replace('\n', '', 7).strip(),
                        # 'book_id':item.xpath(''),
                        'info_url': item.xpath('.//div[1]/a/@href')[0],
                        'img_url': item.xpath('.//div[1]/a/img/@src')[0],
                        'author': author.strip(),
                        'translate': translate,
                        'book_concern': book_concern,
                        'pub_date': pub_date,
                        'assess_count': 0,
                        'score': 0.0,
                        'price': 0.0,
                    }
                except Exception:
                    continue
            #print('未取到有效值，错误原因：', IE)
            # continue
        except Exception as e:
            error_log(e)
            print('未知原因错误：', e)
            continue
        yield book_infos


def save_mysql(all_infos):
    """保存至mysql"""
    pass
    """
    conn = pymysql.Connect(host=host, port=port, user=user, password=pwd, db=db,charset='utf8')
    #建立游标对象
    cursor = conn.cursor()
    #编写sql
    for infos in all_infos:
        print(infos['assess_count'])
        sql = 'insert into douban_books(category, book_name, author, translate, assess_count, score, price, pub_date, book_concern, info_url, img_url)\
        into values("{}", "{}", "{}", "{}", "{}", "{}")'.format(pymysql.escape_string(infos['category']),
        pymysql.escape_string(infos['book_name']), pymysql.escape_string(infos['author']), infos['assess_count'], infos['score'], infos['price'])

        #执行sql
        cursor.execute(sql)

    conn.commit()
    conn.close()
    """


def get_list(all_infos):
    all_list = []
    for infos in all_infos:
        each_list = []
        for key, value in infos.items():  # 对字典items()方法返回的元组列表进行序列解包
            each_list.append(value)

        all_list.append(each_list)  # 返回2维列表，便于保存
    return all_list


def save_csv(info):
    # 获取文件大小
    print(info)
    file_size = os.path.getsize('./books.csv')

    if file_size == 0:
        name = ['类别', '书名', '链接', '图片', '作者',
                '翻译', '出版社', '出版日期', '评论数', '评分', '价格']
        df = pd.DataFrame(data=info, columns=name)  # 创建Datafrma对象
        # 将df写入csv
        df.to_csv('./books.csv', encoding='utf-8', index=False)

    else:
        with open('./books.csv', 'a+', encoding='utf-8', newline='') as file:
            # 创建写入对象
            writer = csv.writer(file)
            writer.writerows(info)


def main():
    """主函数，负责调度"""
    # 生成器
    category_list = []
    for cate in book_category():
        category_list.append(cate)

    l_index = category_list.index('校园')  # 获取校园下标 60
    # 截断表,只要校园之后的
    category_list2 = category_list[l_index+1:]
    # print(category_list2)
    # for cate in book_category():
    for cate in category_list2:
        try:
            print(cate)
            max_page = maxpage(cate)
            print(max_page)

        if maxpage:
            for pa in range(0, max_page):
                html = book_infos(cate, pa)
                if html:
                    lists = parse(html)
                    all_information = parse(html)
                    # for info in all_information:
                    # print(info)
                    info = get_list(all_information)
                    save_csv(info)
                else:
                    continue
        except Exception as e:
            error_log(e)
            print('未知原因错误：', e)
            continue

        # break


if __name__ == '__main__':
    main()
