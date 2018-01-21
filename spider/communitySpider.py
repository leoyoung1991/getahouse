#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import traceback

import requests
import sys
from bs4 import BeautifulSoup
import MySQLdb
import common.common as c
from dao import db
from dao.db_manager import DbManager

reload(sys)
sys.setdefaultencoding('utf8')


class Community:
    __db = None
    __play_url = None
    __headers = None

    def __init__(self, config="../conf/house.conf"):
        self.__db = db.MySQLDB()
        if config != "../conf/house.conf":
            self.__db.setConfig()
        self.__base_community_url = "https://bj.lianjia.com/xiaoqu/"
        self.__page_num = 30
        self.dbManager = DbManager()


    def getOneCommunity(self, com):

        s = requests.session()

        # 拼url 比如东城 获取个数
        com_url = self.__base_community_url + com + '/'
        num = 0
        try:
            s = BeautifulSoup(s.get(com_url).content, "lxml")
            lst = s.find('h2', {'class': 'total fl'})
            num = lst.find('span').text.encode('utf-8')
            print '%s 有 %s 个小区待爬取' % (com, num)
        except Exception as err:
            # 打印异常堆栈
            exstr = traceback.format_exc()
            print exstr
            c.Log('{} : {} {}'.format("ERROR 104 ", "URL", com_url))

        total_page = int(num) / self.__page_num

        for i in range(1, total_page):
            page_com_url = com_url + 'pg' + str(i) + '/'
            try:
                s = requests.session()
                s = BeautifulSoup(s.get(page_com_url).content, "lxml")
                lst = s.find('ul', {'class': 'listContent'})

                values = []
                # 一次插入多条记录
                sql = "insert into community (`name`,`link_community_id`,`image`,`url`,`district`,`address`," \
                      "`building_type`,`year`,`subway_tag`,`price`)" \
                      "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                for play in lst.find_all('li', {'class': 'clear xiaoquListItem'}):

                    try:

                        image = MySQLdb.escape_string(
                            play.find('img', {'class': 'lj-lazy'})['data-original'].encode('utf-8')).strip()

                        title_soup = play.find('div', {'class': 'title'})

                        url = MySQLdb.escape_string(title_soup.find('a')['href'].encode('utf-8')).strip()

                        # congurl中抽取 link_community_id
                        m = re.search('xiaoqu/(.+)/', url)
                        link_community_id = m.group(1).strip()

                        name = MySQLdb.escape_string(title_soup.text.encode('utf-8')).strip().replace("\\n", '')


                        positioninfo_soup = play.find('div', {'class': 'positionInfo'})

                        district = MySQLdb.escape_string(
                            positioninfo_soup.find('a', {'class': 'district'}).text.encode('utf-8')).strip()
                        address = MySQLdb.escape_string(
                            positioninfo_soup.find('a', {'class': 'bizcircle'}).text.encode('utf-8')).strip()

                        building_type_year = MySQLdb.escape_string(
                            play.find('div', {'class': 'positionInfo'}).text.encode('utf-8')).replace("\\n", '')
                        m = re.search('(.+)/(.+)年建成(.+)', building_type_year)

                        # '\\n\\n东城\\n       广渠门 \\n              /塔楼/板楼/塔板结合\\n                  / 1999年建成\\n          '

                        building_type = m.group(1)[m.group(1).index('/') : -1]

                        # 可能是 "未知年建成"
                        year = -1
                        if m.group(2)[2:].decode('utf-8').isdigit():
                            year = int(m.group(2).decode('utf-8'))

                        # 可能不存在
                        subway_tag = ''
                        if play.find('div', {'class': 'tagList'}).find('span') is not None:
                            subway_tag = MySQLdb.escape_string(
                                play.find('div', {'class': 'tagList'}).find('span').text.encode('utf-8')).strip()

                        # 价格可能为 "暂无"
                        price = -1
                        price_str = MySQLdb.escape_string(
                            play.find('div', {'class': 'totalPrice'}).find('span').text.encode('utf-8')).strip()
                        if price_str.isdigit():
                            price = int(price_str)


                        houseinfo_soup = play.find('div', {'class': 'houseInfo'})

                        sale_msg_list = houseinfo_soup.find_all('a')

                        # sale_msg_list 不一定是几个 TODO

                        # on_sale_str =  MySQLdb.escape_string(sale_msg_list[1].text.encode('utf-8'))
                        # m = re.search('u30天成交/(.+)u套', on_sale_str)
                        # on_sale = m.group(1)
                        #
                        # lease_str =  MySQLdb.escape_string(sale_msg_list.get[2].text.encode('utf-8'))
                        # m = re.search('(.+)u套正在出租', lease_str)
                        # lease = m.group(1)
                        values.append((name, link_community_id, image, url, district, address, building_type, year,
                                       subway_tag, price))


                    except Exception as err:
                        # 打印异常堆栈
                        print play
                        exstr = traceback.format_exc()
                        print exstr

                self.dbManager.batchInsertSQL(sql, values)
                print 'page:%s页 小区入库' % i

            except Exception as err:
                # 打印异常堆栈
                exstr = traceback.format_exc()
                print exstr
                c.Log('{} : {} {}'.format("ERROR 104 ", "URL", page_com_url))

    def getAllCommunityList(self, comList):
        for com in comList:
            print '开始爬取区域: %s' % com
            self.getOneCommunity(com)
            print '爬取区域: %s 完成' % com


if __name__ == "__main__":
    tmp = Community()
    interestCom = ['dongcheng', 'xicheng', 'chaoyang', 'haidian', 'changping', 'tongzhou', 'shunyi', 'fengtai',
                   'shijingshan', 'daxing', 'yizhuangkaifaqu', 'fangshan', 'mentougou', 'pinggu', 'huairou', 'miyun',
                   'yanqing', 'yanjiao', 'xiangge']
    tmp.getAllCommunityList(interestCom)
