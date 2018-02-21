#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import threading
import traceback
import datetime
import requests
import sys
from bs4 import BeautifulSoup
import MySQLdb
import common.common as c
from dao import db
from dao.db_manager import DbManager
import time
import random

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
        self.__base_house_url = "https://bj.lianjia.com/ershoufang/"
        self.__page_num = 30
        self.dbManager = DbManager()
        self.multyNum = 2
        self.sleepTime = 0.5
        self.allValidIp = self.getAllValidIp()


    def getOneHouseDetail(self, link_house_source_id, url):

        s = requests.session()
        # requests使用了urllib3库，默认的http connection是keep-alive的，requests设置False关闭。
        s.keep_alive = False

        b = random.sample(self.allValidIp, 1)
        proxy = b[0]

        com_url = self.__base_house_url + str(link_house_source_id) + '.html'
        num = 0
        base_info = ''
        transaction_info = ''

        now = datetime.datetime.now()
        createDay = now.strftime("%Y%m%d")

        try:
            s = BeautifulSoup(s.get(com_url, proxies=proxy).content, "lxml")
            info = s.find('div', {'class': 'introContent'})
            base = info.find('div', {'class': 'base'}).find('div', {'class': 'content'}).find('ul')
            base_info = MySQLdb.escape_string(base.text.encode('utf-8')).strip()

            m = re.search('房屋户型(.+)所在楼层(.+)建筑面积(.+)户型结构(.+)套内面积(.+)建筑类型(.+)房屋朝向(.+)建筑结构(.+)'
                          '装修情况(.+)梯户比例(.+)供暖方式(.+)配备电梯(.+)产权年限(.+)', base_info)

            real_size_str = m.group(5).strip()
            if real_size_str.find('暂无数据') != -1:
                real_size = -1
            else:
                mm = re.search('(.+)㎡(.+)', real_size_str)
                real_size = mm.group(1).strip()

            building_structure = m.group(8).strip().replace("\\n", '')
            fitment_situation = m.group(9).strip().replace("\\n", '')
            stairway_rate = m.group(10).strip().replace("\\n", '')
            heating_way = m.group(11).strip().replace("\\n", '')
            elevator = m.group(12).strip().replace("\\n", '')
            property_right_str = m.group(13).strip().replace("\\n", '')

            mm = re.search('(.+)年', property_right_str)
            property_right = mm.group(1).strip()

            transaction = info.find('div', {'class': 'transaction'}).find('div', {'class': 'content'}).find('ul')
            transaction_info = MySQLdb.escape_string(transaction.text.encode('utf-8')).strip()

            m = re.search('挂牌时间(.+)交易权属(.+)上次交易(.+)房屋用途(.+)房屋年限(.+)产权所属(.+)抵押信息(.+)房本备件(.+)', transaction_info)

            publish_time_str = m.group(1).strip().replace("\\n", '')
            timeArray = time.strptime(publish_time_str, "%Y-%m-%d")
            timeStamp = int(time.mktime(timeArray))
            publish_time = datetime.datetime.fromtimestamp(timeStamp)

            trading_ownership = m.group(2).strip().replace("\\n", '')

            last_transaction_time_str = m.group(3).strip().replace("\\n", '')
            timeArray = time.strptime(last_transaction_time_str, "%Y-%m-%d")
            timeStamp = int(time.mktime(timeArray))
            last_transaction_time = datetime.datetime.fromtimestamp(timeStamp)

            house_usage = m.group(4).strip().replace("\\n", '')
            house_reburn_life = m.group(5).strip().replace("\\n", '')
            property_rights_belong_to = m.group(6).strip().replace("\\n", '')
            mortgage_information = m.group(7).strip().replace("\\n", '')
            room_book = m.group(8).strip().replace("\\n", '')

            sql = "update house_source set real_size = %s, building_structure = %s, fitment_situation = %s, " \
                  "stairway_rate = %s, heating_way = %s, elevator = %s, property_right = %s where link_house_source_id = %s"

            watching_sql = "insert into house_source_sale (`link_house_source_id`, `publish_time`, `last_transaction_time`," \
                           "`trading_ownership`, `house_usage`, `house_reburn_life`, " \
                           "`property_rights_belong_to`, `mortgage_information`, `room_book`, `create_day` ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "



            self.dbManager.execute(sql, (real_size, building_structure, fitment_situation, stairway_rate, heating_way,
                                         elevator, property_right, link_house_source_id))
            self.dbManager.execute(watching_sql, (link_house_source_id, publish_time, last_transaction_time, trading_ownership,
                                                  house_usage, house_reburn_life, property_rights_belong_to, mortgage_information, room_book, createDay))


            print '房源id : %s 更新详细信息成功' % link_house_source_id

        except Exception as err:
            print base_info + '|||' + transaction_info
            # 打印异常堆栈
            exstr = traceback.format_exc()
            print exstr
            c.Log('{} : {} {}'.format("ERROR 104 ", "房源ID", link_house_source_id))

    def getHouseDetailList(self):
        sql = "select link_house_source_id, url from house_source"
        return self.dbManager.queryAll(sql)

        # return self.__db.querySQL(sql)

    def getAllHouseDetail(self, results):

        lens = len(results)
        threads = []

        for house in results:
            t = threading.Thread(target=self.getOneHouseDetail, args=(house.get('link_house_source_id'), house.get('url')))
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
