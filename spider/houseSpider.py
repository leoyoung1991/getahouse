#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import traceback
import datetime
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
        # self.__base_house_list_url = "https://bj.lianjia.com/ershoufang/ng1hu1nb1l2ba50ea90bp200ep320/"
        self.__base_house_list_url = "https://bj.lianjia.com/ershoufang/ng1hu1nb1/"
        self.__page_num = 30
        self.dbManager = DbManager()

    def getHouseList(self):

        s = requests.session()

        # 拼url 获取个数
        com_url = self.__base_house_list_url
        num = 0
        try:
            s = BeautifulSoup(s.get(com_url).content, "lxml")
            lst = s.find('h2', {'class': 'total fl'})
            num = lst.find('span').text.encode('utf-8')
            print '有 %s 个房源待爬取' % num
        except Exception as err:
            # 打印异常堆栈
            exstr = traceback.format_exc()
            print exstr
            c.Log('{} : {} {}'.format("ERROR 104 ", "URL", com_url))

        total_page = int(num) / self.__page_num

        now = datetime.datetime.now()
        createDay = now.strftime("%Y%m%d")

        for i in range(1, total_page):
            page_com_url = com_url + 'pg' + str(i) + '/'
            try:
                s = requests.session()
                s = BeautifulSoup(s.get(page_com_url).content, "lxml")
                lst = s.find('ul', {'class': 'sellListContent'})

                values = []
                watching_values = []
                # 一次插入多条记录
                sql = "insert into house_source (`link_house_source_id`,`url`,`title_discribe`,`community_name`,`link_community_id`,`home_plan_structure`,`building_size`,`orientation`,`decorate_situation`,`elevator`,`floor_situation`,`floor_total`,`building_year`,`building_type`,`address`,`publish_time`,`price`,`total_price`,`real_size`,`building_structure`,`fitment_situation`,`stairway_rate`,`heating_way`,`property_right`,`create_day`)" \
                      "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                watching_sql = "insert into house_source_watching (`link_house_source_id`, `watching_num`, `real_see_num`,`create_day`) values (%s,%s,%s,%s) "

                for play in lst.find_all('li', {'class': 'clear'}):
                    house_info = ''
                    position_info = ''
                    follow_info = ''


                    try:

                        # elevator = Column(String(20), server_default="")
                        #
                        # building_type = Column(String(20), server_default="")
                        # publish_time = Column(DateTime, server_default=func.now())
                        #
                        # # float
                        # real_size = Column(Integer(), server_default=0)
                        # building_structure = Column(String(20), server_default="")
                        # fitment_situation = Column(String(20), server_default="")
                        # stairway_rate = Column(String(20), server_default="")
                        # heating_way = Column(String(20), server_default="")
                        # property_right = Column(Integer(), server_default=0)




                        url = MySQLdb.escape_string(
                            play.find('a', {'class': 'img'})['href'].encode('utf-8')).strip()
                        link_house_source_id = MySQLdb.escape_string(
                            play.find('a', {'class': 'img'})['data-housecode'].encode('utf-8')).strip()

                        image = MySQLdb.escape_string(
                            play.find('img', {'class': 'lj-lazy'})['data-original'].encode('utf-8')).strip()

                        info_soup = play.find('div', {'class': 'info clear'})

                        title_discribe = MySQLdb.escape_string(info_soup.find('div', {'class': 'title'}).text.encode('utf-8')).strip()

                        house_info_soup = info_soup.find('div', {'class': 'address'}).find('div', {'class': 'houseInfo'})

                        community_name = MySQLdb.escape_string(house_info_soup.find('a').text.encode('utf-8')).strip()
                        community_url = MySQLdb.escape_string(house_info_soup.find('a')['href'].encode('utf-8')).strip()
                        m = re.search('xiaoqu/(.+)/', community_url)
                        link_community_id = m.group(1).strip()

                        house_info = MySQLdb.escape_string(house_info_soup.text.encode('utf-8')).strip()


                        # 如果能分五份就五份，六份就六份
                        house_info_split_num = house_info.count('/')

                        if house_info_split_num == 5:
                            m = re.search('(.+)/(.+)/(.+)/(.+)/(.+)/(.+)', house_info)
                            home_plan_structure = m.group(2).strip()
                            size_str = m.group(3).strip()
                            mm = re.search('(.+)平米', size_str)
                            building_size = mm.group(1).strip()
                            orientation = m.group(4).strip()
                            decorate_situation = m.group(5).strip()
                        elif house_info_split_num == 4:
                            m = re.search('(.+)/(.+)/(.+)/(.+)/(.+)', house_info)
                            home_plan_structure = m.group(2).strip()
                            size_str = m.group(3).strip()
                            mm = re.search('(.+)平米', size_str)
                            building_size = mm.group(1).strip()
                            orientation = m.group(4).strip()
                            decorate_situation = m.group(5).strip()



                        position_info = MySQLdb.escape_string(info_soup.find('div', {'class': 'flood'}).find('div', {'class': 'positionInfo'}).text.encode('utf-8')).strip()

                        building_year = -1
                        floor_total = -1
                        if position_info.find('(') != -1:
                            m = re.search('(.+)\((.+)\)/(.+)/(.+)', position_info)
                            floor_situation = m.group(1).strip()
                            floor_total_str = m.group(2).strip()
                            mm = re.search('共(.+)层', floor_total_str)
                            floor_total = mm.group(1).strip()

                            building_year_str = m.group(3).strip()
                            mm = re.search('(.+)年(.+)', building_year_str)
                            if mm is None:
                                building_year = -1
                            else:
                                building_year = mm.group(1).strip()
                            address = m.group(4).strip()
                        else:
                            m = re.search('(.+)/(.+)/(.+)', position_info)
                            floor_situation = m.group(1).strip()
                            floor_total = -1
                            building_year_str = m.group(3).strip()
                            mm = re.search('(.+)年(.+)', building_year_str)
                            if mm is None:
                                building_year = -1
                            else:
                                building_year = mm.group(1).strip()
                            address = m.group(3).strip()




                        follow_info_soup = info_soup.find('div', {'class': 'followInfo'})
                        follow_info = MySQLdb.escape_string(follow_info_soup.text.encode('utf-8')).strip()

                        # 过滤掉一年没卖的房子
                        if follow_info.find('一年前') != -1:
                            continue

                        today = datetime.date.today()
                        if follow_info.find('刚刚') != -1:
                            m = re.search('(.+)人关注/(.+)次带看刚刚发布(.+)', follow_info)
                            watching_num = m.group(1).strip()
                            real_see_num = m.group(2).strip()
                            publish_time = 0
                            real_publish_time = today
                        else:
                            m = re.search('(.+)人关注/(.+)次带看(.+)以前发布(.+)', follow_info)
                            watching_num = m.group(1).strip()
                            real_see_num = m.group(2).strip()
                            # 计算发布时间 天/月
                            publish_time = m.group(3).strip()
                            mm = re.search('(.+)天', publish_time)
                            if mm is None:
                                mmm = re.search('(.+)个月', publish_time)
                                days_ago = mmm.group(1).strip()
                            else:
                                days_ago = mm.group(1).strip()
                            real_publish_time = today - datetime.timedelta(int(days_ago))


                        price_info_soup = info_soup.find('div', {'class': 'priceInfo'})

                        total_price = MySQLdb.escape_string(price_info_soup.find('div', {'class': 'totalPrice'}).find('span').text.encode('utf-8')).strip()
                        total_price = float(total_price) * 10000
                        price_str = MySQLdb.escape_string(price_info_soup.find('div', {'class': 'unitPrice'}).find('span').text.encode('utf-8')).strip()
                        m = re.search('单价(.+)元/平米', price_str)
                        price = m.group(1).strip()

                        #elevator，building_type，real_size,building_structure,fitment_situation,stairway_rate,heating_way,property_right 在列表中获取不到，需要到详情去获取

                        values.append((link_house_source_id,url,title_discribe,community_name,link_community_id,
                                       home_plan_structure,building_size,orientation,decorate_situation,'',floor_situation,
                                       floor_total,building_year,'',address,real_publish_time,price,total_price,
                                       0,'','','',
                                       '',0, createDay))

                        watching_values.append((link_house_source_id, watching_num, real_see_num, createDay))


                    except Exception as err:
                        # 打印异常堆栈
                        print house_info + '|||' + position_info + '|||' + follow_info
                        exstr = traceback.format_exc()
                        print exstr

                self.dbManager.batchInsertSQL(sql, values)
                self.dbManager.batchInsertSQL(watching_sql, watching_values)
                print 'page:%s页 房源入库' % i

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

    # 后续扩展可以考虑把钱什么的算进去入参

    tmp.getHouseList()
