#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.sql import func
import config

Base = declarative_base()


class Community(Base):
    __tablename__ = "community"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(30), server_default="")
    link_community_id = Column(Integer(), server_default=0)
    image = Column(String(500), server_default="")
    url = Column(String(500), server_default="")
    district = Column(String(20), server_default="")
    address = Column(String(10), server_default="")
    building_type = Column(String(50), server_default="")
    year = Column(Integer(), server_default=0)
    subway_tag = Column(String(50), server_default="")
    price = Column(Integer(), server_default=0)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now())


class CommunitySale(Base):
    __tablename__ = "community_sale"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    link_community_id = Column(Integer(), server_default=0)
    month_deal = Column(Integer(), server_default=0)
    on_sale = Column(Integer(), server_default=0)
    lease = Column(Integer(), server_default=0)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now())


class HouseSource(Base):
    __tablename__ = "house_source"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    link_house_source_id = Column(Integer(), server_default=0)
    url = Column(String(500), server_default="")
    title_discribe = Column(String(500), server_default="")
    community_name = Column(String(30), server_default="")
    link_community_id = Column(Integer(), server_default=0)
    home_plan_structure = Column(String(20), server_default="")
    # float
    size = Column(Integer(), server_default=0)
    orientation = Column(String(20), server_default="")
    decorate_situation = Column(String(20), server_default="")
    elevator = Column(String(20), server_default="")
    floor_situation = Column(String(20), server_default="")
    floor_total = Column(Integer(), server_default=0)
    building_year = Column(Integer(), server_default=0)
    building_type = Column(String(20), server_default="")
    address = Column(String(20), server_default="")
    publish_time = Column(DateTime, server_default=func.now())
    price = Column(Integer(), server_default=0)
    total_price = Column(Integer(), server_default=0)
    # float
    real_size = Column(Integer(), server_default=0)
    building_structure = Column(String(20), server_default="")
    fitment_situation = Column(String(20), server_default="")
    stairway_rate = Column(String(20), server_default="")
    heating_way = Column(String(20), server_default="")
    property_right = Column(Integer(), server_default=0)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now())


class HouseSourceWatching(Base):
    __tablename__ = "house_source_watching"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    link_house_source_id = Column(Integer(), server_default=0)
    watching_num = Column(Integer(), server_default=0)
    real_see_num = Column(Integer(), server_default=0)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now())


class HouseSourceSale(Base):
    __tablename__ = "house_source_sale"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    link_house_source_id = Column(Integer(), server_default=0)
    publish_time = Column(DateTime, server_default=func.now())
    last_transaction_time = Column(DateTime, server_default=func.now())
    trading_ownership = Column(String(30), server_default="")
    house_usage = Column(String(30), server_default="")
    house_reburn_life = Column(String(30), server_default="")
    property_rights_belong_to = Column(String(30), server_default="")
    mortgage_information = Column(String(30), server_default="")
    room_book = Column(String(30), server_default="")
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now())


engine = create_engine(config.get_db(), convert_unicode=True, echo=True)


def single(table, k, v):
    cnt = engine.execute('select count(*) from ' + table + ' where ' + k + '="' + v + '"').fetchone()
    if cnt[0] == 0:
        return True
    else:
        return False


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print(single("playlist163", "link", "sd"))
