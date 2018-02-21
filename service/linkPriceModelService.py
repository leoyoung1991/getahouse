#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import threading
import traceback
import requests
import sys
import common.common as c
from dao import db
from dao.db_manager import DbManager
import time
import random
import urllib2
import json

reload(sys)
sys.setdefaultencoding('utf8')


class HouseDetailSpider:
    __db = None
    __play_url = None
    __headers = None

    def __init__(self, config="../conf/house.conf"):
        self.__db = db.MySQLDB()
        if config != "../conf/house.conf":
            self.__db.setConfig()
        self.__base_house_url = "https://bj.lianjia.com/yezhu/gujiaview/?channel_id=6"
        self.__page_num = 30
        self.dbManager = DbManager()
        self.multyNum = 5
        self.sleepTime = 1
        self.allValidIp = self.getAllValidIp()

        self.opener = urllib2.build_opener()
        self.opener.addheaders.append(('Cookie',
                                       'clouddba-web_USER_COOKIE=1B26963AA530BBB8BF1C472638445D86CD08EE20473BF9DD2B5E56F98B131CF82BCFEFDE1CF8140BCC152AFE609928109FE52F8AD954025B8B363479C43FBC022C5BD16AAF39B0C88BDA2A0D860F8F2FE69C794AAF3479AE3D94B42690F3D1BAF8ABE19D7216ACC85FCB9433166972C9B415CA99243D054D947F46B9003D994761093835D078E8728BBB81B636510A7595A7E07F65422BA2DE94BA3CF01F81B3401F8BAADBCABA3C9E46D82D154A3DFFD3AF1150A4EF9E5AD30FD43FCC9FD2CBF472E5078E5061E2CDFB6ADE68280D981BCFC57CE458FA813F2CB9AC4D5CD2AD927A39CD5E5E0C3D23BB4DF5F5E28CFBF760B271E71CDABFEA7FA34BB3853B6EB7C0AD821691D3C98ED4DF14280AE193AEFF255D5AE58A72B7C2392971B8090B749987AA651D1FEC006519496CED3E7CCE7C7BAFB53828E54DCF923003A444516132DA16AA21AFE27AEF7834D481F472C79E446C133F326AAB4C37F197D328D857AB33740114241B86DE74CD4F2F1919CF005D0D96532D8537CEEC6498EC197FD3FF352A40EEB38AD8CD982AC33570DA; clouddba-web_SSO_TOKEN=BB8DDB7131E7C59C7DF9AB1F35A801782BC2A74A011226D2BDE475958DA6F0842EE0C11C5218342CAC8AB471D04AFDCF; clouddba-web_LANG=zh-CN; clouddba-web_LAST_HEART_BEAT_TIME=76B71D3EAB8836708EA23BB3D397B8DC; __CloudDBA_USER_TOKEN_KEY_=ed20a4d4-6035-4a4e-adfe-9f596989ab52; UM_distinctid=15f2e01f769991-0802eddc727d94-31627c00-13c680-15f2e01f76ace4; cna=+ddtEvfySTECAYzNHAhqB9eb; isg=AnFxLJM5jOYS_SDyKslnalZpgPsVK_18VEvzgVOGoDhwepPMm62EoH7Y6jjn'))

    def getOneHouseDetail(self, link_house_source_id, url, link_community_id, home_plan_structure, building_size,
                          floor_situation, floor_total, building_year, community_name, orientation):

        s = requests.session()
        # requests使用了urllib3库，默认的http connection是keep-alive的，requests设置False关闭。
        s.keep_alive = False

        b = random.sample(self.allValidIp, 1)
        proxy = b[0]
        # 楼层转化

        # building_year  floor_total 可能为 -1
        floor_total = 6
        if building_year == -1:
            building_year = 1980
        if floor_total == -1:
            floor_total = 6

        if floor_situation == '中楼层':
            floor = int(floor_total) / 2
        elif floor_situation == '底层':
            floor = 1
        elif floor_situation == '顶层':
            floor = floor_total
        elif floor_situation == '低楼层':
            floor = int(floor_total) / 4
        elif floor_situation == '高楼层':
            floor = int(floor_total) / 4 * 3
        else:
            floor = floor_total

        # 朝向英文转化
        ori = ''
        if orientation.find('东') != -1:
            ori += 'east'
        elif orientation.find('西') != -1:
            ori += 'west'
        elif orientation.find('南') != -1:
            ori += 'south'
        elif orientation.find('北') != -1:
            ori += 'north'

        # 卧室客厅厕所数量
        room_count = 2
        hall_count = 1
        toilet_count = 1

        com_url = self.__base_house_url + '&community_id=' + str(link_community_id) + '&room_count=' + str(
            room_count) + '&hall_count=' + str(hall_count) + '&toilet_count=' + str(toilet_count) + '&area=' + str(
            building_size) + '&total_floor=' + str(floor_total) + '&build_finish_year=' + str(
            building_year) + '&community_name=' + str(community_name) + '&orientation=' + str(ori) + '&floor=' + str(
            floor)

        base_info = ''
        transaction_info = ''

        try:

            f = self.opener.open(com_url)
            content = f.read()

            # main.init({"info": {"total_price": "2681340.56", "total_price_range": [2547273.532, 2815407.588],
            #                     "month": "201801", "unit_price": 44689, "type": "month", "month_trans": "-0.060"},
            #            "gujia_id": "15165302791746950531", "community_id": "1111027376017", "bizcircle_id": 18335727,
            #            "bizcircle_name": "\u56db\u60e0", "community_name": ""})

            m = re.search('main.init\({"info":(.+),"gujia_id"', content)
            info_json = m.group(1).strip()
            j = json.loads(info_json)
            appraisal = j['total_price']
            print appraisal

            sql = "update house_source set link_model_price = %s where link_house_source_id = %s"

            self.dbManager.execute(sql, (appraisal, link_house_source_id))

            print '房源id : %s 更新链家模型价格成功' % link_house_source_id

        except Exception as err:
            print str(link_house_source_id) + '|||' + com_url
            # 打印异常堆栈
            exstr = traceback.format_exc()
            print exstr
            c.Log('{} : {} {}'.format("ERROR 104 ", "房源ID", link_house_source_id))

    def getHouseDetailList(self):
        sql = "select link_house_source_id, url, link_community_id, home_plan_structure, building_size, floor_situation, floor_total, building_year, community_name, orientation from house_source "
        return self.dbManager.queryAll(sql)

        # return self.__db.querySQL(sql)

    def getAllHouseDetail(self, results):

        lens = len(results)
        threads = []

        for house in results:
            t = threading.Thread(target=self.getOneHouseDetail,
                                 args=(house.get('link_house_source_id'), house.get('url'),
                                       house.get('link_community_id'), house.get('home_plan_structure'),
                                       house.get('building_size'), house.get('floor_situation'),
                                       house.get('floor_total'), house.get('building_year'),
                                       house.get('community_name'), house.get('orientation')))
            threads.append(t)

        i = 0
        for t in threads:
            t.setDaemon(True)
            t.start()
            # 多线程并发+休息
            i += 1
            if i >= self.multyNum:
                time.sleep(self.sleepTime)
                i = 0
        print '抓取所有房源详细信息线程全部启动成功。。。'

        for t in threads:
            t.join()

    def getAllValidIp(self):
        # f = open("../common/antiSpider/ipProxy/valid_proxy")
        f = open("/home/work/getahouse/common/antiSpider/ipProxy/valid_proxy")
        lines = f.readlines()
        proxys = []
        for i in range(0, len(lines)):
            ip = lines[i].strip("\n").split(":")
            proxy_host = "http://" + ip[0] + ":" + ip[1]
            proxy_temp = {"http": proxy_host}
            proxys.append(proxy_temp)
        return proxys


if __name__ == "__main__":
    tmp = HouseDetailSpider()

    # 后续扩展可以考虑把钱什么的算进去入参
    results = tmp.getHouseDetailList()
    tmp.getAllHouseDetail(results)
