import re
import time
import requests
import logging
import datetime
import traceback

from urllib import parse

import pandas as pd

from db_operations import MysqlOperat
from config import get_config


class Log:
    """ 创建日志模块 """
    # 级别：critical > error > warning > info > debug,notset
    def __init__(self, logfile='./logging.log'):
        self.logger = logging.getLogger(__name__)
        self.logfile = logfile   # 日志存储路径
        self.logger.setLevel(level=logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # 控制写入文件
        hd = logging.FileHandler(self.logfile, encoding='utf-8')
        # hd.setLevel(logging.INFO)
        hd.setFormatter(formatter)
        
        # 控制屏幕输出
        sh = logging.StreamHandler()
        # sh.setLevel(logging.INFO)
        sh.setFormatter(formatter)

        # 将配置参数添加都对象中
        self.logger.addHandler(hd)
        self.logger.addHandler(sh)

    @property
    def getlog(self):
        return self.logger


def unescape(content):
    """ urlencoded 内容解码 """
    content = content.replace('%u', '\\u')
    return parse.unquote(content.encode().decode('unicode-escape'))


class KongQi:
    def __init__(self) -> None:
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Connection': 'keep-alive',
            # 'Cookie': '_dx_uzZo5y=4d3bfcd4b7666d8573bd9345cd0a1793835d74eab4bb5c22244b5d72de1999c9e2a52654; _dx_app_81e16deaf5fee41ed38834363824b3e3=5f4616e1ePquA7BQa4pCkGD8lGeUCss652QXWMU1; __utmz=105455707.1598429128.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _dx_captcha_vid=82A769D5DE548F88D522001ED59EF0FC8E9E444D896653FA9093A55B8D40BCBE5383D37BB8309D1BD3A2F6D2D4FC7494BEC71E968DB5237A0EAE35941AFF0AC6B873A755DAE116BDC326D5BCA2EE3476; .ASPXAUTH=763488D9809F9C709BE03ABC9D60AEFCDC9EE4414837A3BBE0B0CF5D312055ABB847828CE09B8F889A66ED9F182014558A62F733882460EEB0CC322A49B4E4DC0E764B665B5E135EC70006C764AD4A03A49163CB055A43AA3525919E30B207E54A5C5FFEF1247339E9198373A0038CAB7DF053CEACAD7C2E6719F98FFE662D739972D93B6F8C582B174E3EC7792BD24A194EB44D2F17CA87C79E93FD96C1256FF282CA4431AB14EA95CA9FDA; Hm_lvt_7ad5a3f0ba646f5864e788025aab20a2=1598429128,1599130329,1599446187; __utma=105455707.729037864.1598429128.1599130329.1599446187.3; __utmc=105455707; ajaxkey=29746F5A6761AE720C1112200AB530CEA27C216D265CC058; Hm_lpvt_7ad5a3f0ba646f5864e788025aab20a2=1599446192; acw_tc=7b39758215994608549595229eef8130e7d27970e8160d41d11b1ba32c01cd; SERVERID=63ce6a224eb1e4e64c95f4d7b348be8a|1599460855|1599460854',
            'Host': 'www.ipe.org.cn',
            'Origin': 'http://www.ipe.org.cn',
            'Referer': 'http://www.ipe.org.cn/AirMap_fxy/AirMap.html?q=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        self.form_data = {
            'headers[Cookie]': '_dx_uzZo5y=4d3bfcd4b7666d8573bd9345cd0a1793835d74eab4bb5c22244b5d72de1999c9e2a52654; _dx_app_81e16deaf5fee41ed38834363824b3e3=5f4616e1ePquA7BQa4pCkGD8lGeUCss652QXWMU1; __utmz=105455707.1598429128.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _dx_captcha_vid=82A769D5DE548F88D522001ED59EF0FC8E9E444D896653FA9093A55B8D40BCBE5383D37BB8309D1BD3A2F6D2D4FC7494BEC71E968DB5237A0EAE35941AFF0AC6B873A755DAE116BDC326D5BCA2EE3476; Hm_lvt_7ad5a3f0ba646f5864e788025aab20a2=1598429128,1599130329,1599446187; __utma=105455707.729037864.1598429128.1599130329.1599446187.3; __utmc=105455707; __utmt=1; ajaxkey=29746F5A6761AE720C1112200AB530CEA27C216D265CC058; __utmb=105455707.2.10.1599446187; Hm_lpvt_7ad5a3f0ba646f5864e788025aab20a2=1599446192; SERVERID=8abfb74b5c7dce7c6fa0fa50eb3d63af|1599446204|1599446177',
            'cmd': 'getSpaceAQI',
            'searchTxt': '',
            'province': '0',
            'city': '0',
            'level': '5',
            'mapprovince': '',
            'nostr': '',
            'indexname': 'aqi',
            'keycode': '4543j9f9ri334233r3rixxxyyo12',
            'time': '2020/9/5 10:00:00'
        }

    def post(self, form_data):
        resp = requests.post(
            'http://www.ipe.org.cn/data_ashx/GetAirData.ashx?xx=getSpaceAQI',
            data=form_data,
            headers=self.headers
        )
        resp.raise_for_status()
        return resp

    def parse_data(self, resp):
        data_str = unescape(resp.content.decode('utf-8'))
        data = re.search('\[.*\]', data_str)
        df = pd.DataFrame(eval(data.group()))
        df.columns = [
            'SITE_ID', 'LAT', 'LON', 'DEGREE', self.form_data['indexname']]
        # df.to_csv('./1.csv', index=False)
        return df


def main(hour):
    kongqi = KongQi()
    mysql = MysqlOperat()
    zhibiao = ['pm2_5', 'pm10', 'so2', 'no2', 'o3', 'co', 'aqi']
    for parm in zhibiao:
        kongqi.form_data['indexname'] = parm
        kongqi.form_data['time'] = hour

        resp = kongqi.post(kongqi.form_data)
        data = kongqi.parse_data(resp)
        # 插入时间
        data['time'] = hour
        table_name = get_config().get('table_name', parm)
        data.to_csv('1.csv', index=False)
        # mysql.insert(data, table_name)
        time.sleep(2)
        break

        # 写入数据库 分表写入


if __name__ == "__main__":
    # kongqi = KongQi()
    # resp = kongqi.post(kongqi.form_data)
    # print(unescape(resp.content.decode('utf-8')))
    # kongqi.parse_data(resp)
    # hour_list = pd.date_range(start='9/6/2020', end='10/9/2020', freq='h')
    
    start_date = (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    hour_list = pd.date_range(start=start_date, periods=24, freq='h')
    for hour in hour_list:
        hour_str = str(hour).replace('-', '/')
        main(hour_str)
        time.sleep(5)
        break
