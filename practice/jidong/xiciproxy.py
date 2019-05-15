import requests, re 
import requests, re 
from pyquery import PyQuery as pq 
from lxml import etree
import subprocess as sp  #可以用于执行cmd命令，如sp.Popen('tasklist'),详细参数见文末

class daili:

    def get_proxy(self):
    #url拼接，占位符、连接符、格式化输出符
    #url = 'http://www.xicidaili.com/nn/%d/' % page
    #url = 'http://www.xicidaili.com/nn/' + str(page)
        self.url = 'http://www.xicidaili.com/nn/1/'
        self.head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',}
        try:
            res = requests.get(self.url, headers = self.head)
            if res.status_code == 200:
                html = res.text
                #print(res.status_code)
        except:
            print('出错了！')

        #解析网页
        doc = pq(html)
        items = doc('#ip_list tr')
        del items[0]
        #items = etree.HTML(str(items))
        i = 0
        self.proxy_list=[]
        for item in items.items():
            #print(item)
            aa = etree.HTML(str(item))
            ip = aa.xpath('//td[2]/text()')[0]
            port = aa.xpath('//td[3]/text()')[0]
            #ip = item.find('td:eq(2)').text()
            #print(ip)
            self.proxy_list.append(ip + ':' + port)

        return self.proxy_list


    def check_ip(self, ip):
        """使用windows系统的cmd命令 ping 查看返回值来检验"""
        #创建cmd命令，请求次数，每次请求最长等待时间
        cmd = 'ping -n 3 -w 3 {}'.format(self.ip)
        #传入管道参数，将shell设为真后，响应内容可以被输出
        p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        #获得相应结果，并解码
        out = p.stdout.read().decode("gbk")
        #获取丢包数，如果丢包数为0，则表明代理通畅，可用，否则抛弃
        lose = re.findall(u'丢失 = ([0-9]+)', out, re.IGNORECASE)
        #print(lose)

        if lose[0] == '0':
            self.average_time = re.findall(u'平均 = ([0-9]+)ms', out, re.IGNORECASE)
            #print(average_time)

        else:
            return 1000
        return int(self.average_time[0])

    def get_ip(self):
        proxy_list = self.get_proxy()
        for i in range(len(self.proxy_list)):
            proxy = self.proxy_list[i]
            self.ip = proxy.split(':')[0]  #分割出ip
            #print(ip)
            self.avg = self.check_ip(self.ip)  #执行校验函数

            #根据返回结果，将不可用代理从列表中删除
            if self.avg < 200:
                #print('代理可用：', proxy)
                return proxy
                break

            