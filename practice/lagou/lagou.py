# 爬取拉勾网信息，存储并分析  https://www.lagou.com/
# 分析：拉勾网页面请求为ajxs请求，方式为post,带3个参数，响应结果为json
import requests
import time
import json
import pandas as pd
import os
import csv


def file_save(info):
    '''数据以csv形式存储起来'''
    file_size = os.path.getsize(r'.\lagou_1.csv')  # 获取目标文件大小
    # print(file_size)
    if file_size == 0:
        # 表头
        name = ['职位id', '工作年限', '学历', '薪水', '城市']
        # 建立DataFrame对象
        # DataFrame中有两个参数，均是列表
        file_test = pd.DataFrame(columns=name, data=info)
        file_test.to_csv(r'.\lagou_1.csv', encoding='gbk',
                         index=False)  # 使用to_csv方法将数据写入
    else:  # 不需要创建表头
        with open(r'.\lagou_1.csv', 'a+', newline='') as file_test:
            # 初始化写入文件，传入句柄，调用 writerows方法
            writer = csv.writer(file_test)
            writer.writerows(info)  # writerow 单行写入，writerows多行写入，列表为二维列表

# 取网页数据模块


def get_page():
    # 请求网址
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    # 请求头
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        # 'Content-Length':'44',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?labelWords=sug&fromSearch=true&suginput=python',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': None,
        'X-Requested-With': 'XMLHttpRequest',
    }

    # 遍历所有的相关页
    for i in range(1, 25):
        data = {
            'first': 'false',
            'kd': 'python爬虫',
            'pn': i,
        }

        # 发送请求
        req = requests.post(url, data=data, headers=headers)
        req.encoding = 'UTF-8'  # 解码
        req_result = req.json()
        print("第%d页，状态码：" % i, req.status_code)
        # print(req_result.get('code'))

        # 定位数据位置
        data = req_result['content']['positionResult']['result']
        # 遍历数据并封装至列表中
        list_info = []
        for k in range(0, len(data)):
            positionId = data[k].get('positionId')
            workYear = data[k].get('workYear')
            education = data[k].get('education')
            city = data[k].get('city')
            salary = data[k].get('salary')
            list_one = [positionId, workYear, education, salary, city]
            list_info.append(list_one)
        print(list_info)

        # 调用文件写入方法
        file_save(list_info)
        print('等待中……')
        time.sleep(2.5)


'''
        return req_result

def get_info(result):
    #定位数据位置
    data = result['content']['positionResult']['result']
    #print(data)

    #遍历,生成器
    for k in range(0, 15):
        yield{
            'createTime':data[k].get('createTime'),
            'positionId':data[k].get('positionId'),
            'workYear':data[k].get('workYear'),
            'education':data[k].get('education'),
            'city':data[k].get('city'),
            'positionName':data[k].get('positionName'),
            'salary':data[k].get('salary'),
        }
'''

# 存储至csv中方便调用


def main():
    result = get_page()


if __name__ == '__main__':
    main()
