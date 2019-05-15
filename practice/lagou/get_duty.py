import csv, time, re
import requests
from lxml import etree
from random import randint

position_urls = []
headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection':'keep-alive',
    #'Content-Length':'44',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie':'_ga=GA1.2.966205375.1543326020; user_trace_token=20181127214019-fb37f405-f249-11e8-8c28-5254005c3644; LGUID=20181127214019-fb37f939-f249-11e8-8c28-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1543415586,1543415591,1543498664,1543638653; index_location_city=%E5%85%A8%E5%9B%BD; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221675abc57b2292-04f82ede2b58248-1160684a-921600-1675abc57b3246%22%2C%22%24device_id%22%3A%221675abc57b2292-04f82ede2b58248-1160684a-921600-1675abc57b3246%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; JSESSIONID=ABAAABAAAGGABCB18695AB38F65F9D99F6BADADC93A9AB5; LGSID=20181201123052-e2dbba3e-f521-11e8-8ca7-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fts%3D1543638651462%26serviceId%3Dlagou%26service%3Dhttp%25253A%25252F%25252Fwww.lagou.com%25252Fjobs%25252F%26action%3Dlogin%26signature%3D10D64BF94E37245594C5DE220F961099; LGRID=20181201123117-f1ef94ad-f521-11e8-8ca7-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1543638678; _gid=GA1.2.561125281.1543638655; _gat=1; SEARCH_ID=241a6c03e84a411c90c9609fe4391727',
    'Host':'www.lagou.com',
    'Referer':'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?labelWords=sug&fromSearch=true&suginput=python',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
    'X-Anit-Forge-Code':'0',
    'X-Anit-Forge-Token':None,
    'X-Requested-With':'XMLHttpRequest',
    }

def read_csv():
    """读取csv文件"""
    with open('./lagou_1.csv', 'r', newline = '') as csvfile:
        content = csv.reader(csvfile)
        
        i = 0 #用来剔除文件表头，并计数
        for row in content:
            #print(row) 
            if i != 0:  #i = 0时，数据为表头
                position_url = 'https://www.lagou.com/jobs/{}.html'.format(row[0])
                #print(position_url)
                position_urls.append(position_url)                
            i += 1 #计数

        print('总共%d个职位信息' % int(i-1))
  
        #print(position_urls)

def write_file(text):

    with open('./duty.txt', 'a+') as f:
        f.write(text)

def write_file2(text):
    with open('./requirement.txt', 'a+', encoding = 'gbk') as f:

        f.write(text)


def get_duty():
    """获取详细的职业信息"""
    index = 0
    for url in position_urls:
        #print(url)
        work_duty = ''
        work_requirement = ''

        req = requests.get(url, headers = headers)
        html = etree.HTML(req.text)

        result = html.xpath('//dl[@id="job_detail"]/dd[2]/div//p/text()')
        #print(result)
        #write_file(result)
        time.sleep(randint(0, 5))
        
        """
        index += 1
        if index == 5:
            break
        """
        
        # 数据清理
        #j = 0
        for i in range(len(result)):

            result[i] = result[i].replace('\xa0', ' ')  #使用空格将字符串中的‘\xa0’替换，此方法可以用于解决编码问题
            result[i] = result[i].replace('\u2022','')
            result[i] = result[i].replace('\xd8','')
            if result[i][0].isdigit():#判断字符串是否为数字
                #if j == 0:
                    #result[i] =result[i][2:].replace('、', ' ')#第一个是数字,则从第二个开始截断，替换顿号
                    #result[i] = re.sub('[;；.0-9。]', '', result[i]) #re.sub()将匹配到的内容，替换
                    #work_duty = work_duty + result[i] + '/' #在每条要求后增加
                    #j = j + 1
                
                #字符串的第一个数字为1，则说明到了岗位要求
                #elif result[i][0] == '1' and not result[i][1].isdigit():
                #    break  
                #else:
                result[i] = result[i][2:].replace('、', ' ')
                result[i] = re.sub('[、；;.0-9。]','', result[i])
                    #resuil[i] = result[i].replace['岗位职责']
                work_duty = work_duty + result[i]+ '/'
            else:
                result[i] = re.sub('[;；.0-9。]', '', result[i])
                work_duty = work_duty + result[i] + '/'

                #j = j + 1


        m = i
        # 岗位职责
        write_file(work_duty)
        print(work_duty)
'''
        # 数据清理
        j = 0
        for i in range(m,len(result)):
            result[i] = result[i].replace('\xa0',' ')  #替换gbk无法解码的字符
            result[i] = result[i].replace('\u2022',' ')
            if result[i][0].isdigit():  #判断第一个字符是否是数字
                if j == 0:
                    result[i] = result[i][2:].replace('、', ' ')#将字符串从第二个字符开始截断，并将里面的、以空格替代，再将结果返回给result[i]
                    result[i] = re.sub('[、；;.0-9。]', '', result[i]) #正则匹配其中的中文标点，替代为空字符
                    work_requirement = work_requirement + result[i] + '/' #传入字符串中
                    j = j + 1
                elif result[i][0] == '1' and not result[i][1].isdigit():
                    # 控制范围
                    break
                else:
                    result[i] = result[i][2:].replace('、', ' ')
                    result[i] = re.sub('[、；;.0-9。]', '', result[i])
                    work_requirement = work_requirement + result[i] + '/'
        # 岗位要求
        write_file2(work_requirement)
        print(work_requirement)
        print("-----------------------------")
            
        #print(result)
        break
'''

if __name__ == '__main__':
    read_csv()
    get_duty()