import time
import traceback
import urllib.request as urllib2
import uuid
from urllib.request import Request

import pyamf
from pyamf import remoting
from pyamf.flex import messaging

from config import get_config
from db_operations import MysqlOperat, Log


# com.fpi.prj.zjemc.airenv.wms.entity.vo.WmsFlexDayDataVo
class WmsHourDataVo:
    def __init__(self):
        None


class Zjemc:
    """ 浙江省水质实时数据采集 """
    pyamf.register_class(
        WmsHourDataVo,
        alias='com.fpi.prj.zjemc.airenv.wms.entity.vo'
    )
    msg = messaging.RemotingMessage(
        messageId=str(uuid.uuid1()).upper(),
        clientId=str(uuid.uuid1()).upper(),
        operation='getAllShowHourData',  # getAllValleyVo\getAllSiteHistoryVo
        destination='GISCommonDataUtilForWms',
        timeToLive=0,
        timestamp=0,
    )

    def __init__(self) -> None:
        self.headers = {
            # POST /wms/messagebroker/amfWms HTTP/1.1
            'Host': 'wms.zjemc.org.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'Content-Type': 'application/x-amf',
            'Accept': '*/*',
            'Origin': 'http://wms.zjemc.org.cn',
            'X-Requested-With': 'ShockwaveFlash/32.0.0.445',
            # Referer	http://wms.zjemc.org.cn/wms/wmsflex/index.swf/[[DYNAMIC]]/4
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

    def getRequestData(self):
        Zjemc.msg.body = []
        Zjemc.msg.headers['DSEndpoint'] = None
        Zjemc.msg.headers['DSId'] = str(uuid.uuid1()).upper()
        # 按AMF协议编码数据
        req = remoting.Request('null', body=(Zjemc.msg,))
        env = remoting.Envelope(amfVersion=pyamf.AMF3)
        env.bodies = [('/1', req)]
        data = bytes(remoting.encode(env).read())
        return data

    def getResponse(self, data):
        url = 'http://wms.zjemc.org.cn/wms/messagebroker/amf'
        resp = Request(url, data, self.headers)
        # resp = requests.post(
        #     url,
        #     data=data,
        #     headers=self.headers
        # )
        # 解析返回数据
        opener = urllib2.build_opener()
        return opener.open(resp).read()
        # return resp

    def getContent(self, response):
        amf_parse_info = remoting.decode(response)
        info = amf_parse_info.bodies[0][1].body.body
        # print(info)
        factor_key = ['pH', 'DO（mg/l）', 'COD_Mn（mg/l）', 'TP（mg/l）', 'NH3-N（mg/l）']
        level_key = ['pH_级别', 'DO_级别', 'COD_Mn_级别', 'TP_级别', 'NH3-N_级别']
        data_list = []
        for record in info:
            # print(record)
            data = {}
            data['监测站点'] = record['mtName']
            data['监测时间'] = record['monitorTime']
            data['所属区域'] = record['boundaryArea']
            data['longitude'] = record['longitude']
            data['latitude'] = record['latitude']
            factor_value = eval(str(record['factorValues'])[35:-1])
            level_value = eval(str(record['factorLevel'])[35:-1])

            for key, value in zip(factor_key, factor_value):
                data[key] = value
            
            for key, value in zip(level_key, level_value):
                data[key] = value

            data_list.append((data))

        return data_list


def main():
    logger = Log('./longging_3.log').getlog
    try:
        zj = Zjemc()
        mysql = MysqlOperat()
        data = zj.getRequestData()
        resp = zj.getResponse(data)
        result = zj.getContent(resp)

        mysql.insert(result, get_config().get('table_name', 'zjdbsjc'), lt=True)
    except Exception:
        logger.info(traceback.format_exc())

   
if __name__ == "__main__":
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '开始采集'.center(80, '*'))
    main()
    # print(result)  # [35:-1]
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '采集完成'.center(80, '*'))
