import time

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy import and_
from api import guess
from sqlalchemy.sql import func
from sqlalchemy.orm import load_only
import re
import random
from common import *
Base = declarative_base()

class Province(Base):
    __tablename__ = 'province'
    _id = Column(Integer, primary_key=True)
    name = Column(String(64))
    province_id = Column(String(12))
    children = relationship('City')

class City(Base):
    __tablename__ = 'city'
    _id=Column(Integer,primary_key=True)
    name = Column(String(64))
    city_id = Column(String(12))
    province_id = Column(String(12), ForeignKey('province.province_id'))
    children = relationship('Country')
    parent = relationship("Province")

class Country(Base):
    __tablename__ = 'country'
    _id = Column(Integer, primary_key=True)
    name = Column(String(64))
    country_id = Column(String(12))
    city_id = Column(String(12), ForeignKey('city.city_id'))
    children = relationship('Town')
    parent = relationship("City")

class Town(Base):
    __tablename__ = 'town'
    _id = Column(Integer, primary_key=True)
    name = Column(String(64))
    town_id = Column(String(12))
    country_id = Column(String, ForeignKey('country.country_id'))
    children = relationship('Village')
    parent = relationship("Country")

class Village(Base):
    __tablename__ = 'village'
    _id = Column(Integer, primary_key=True)
    name = Column(String(64))
    village_id = Column(String(12))
    town_id = Column(String, ForeignKey('town.town_id'))
    parent = relationship("Town")

class GuestAddress(Base):
    __tablename__ = 'guest_address'
    _id = Column(Integer, primary_key=True)
    name = Column(String(64))
    village_id = Column(String, ForeignKey("village.village_id"))
    parent = relationship("Village")

pattern=re.compile(r"\d")
def qualifyGuessAddress(address):
    qualify=False
    if pattern.search(address) is not None:
        qualify=True
    if "村" in address:
        qualify=True
    return qualify

class Entry(Base):
    __tablename__ = 'entry'
    _id = Column(Integer, primary_key=True)
    name = Column(String(6))
    phone = Column(String(12))
    province = Column(String(12))
    city = Column(String(12))
    country = Column(String(12))
    town = Column(String(12))
    detail_address = Column(String(256))
    composed_string = Column(String(1024))

    def compose_string(self):
        province = self.province
        city = self.city
        if (province[-1] == "省") and random.random() < 0.3:
            province = province[0:-1]
        if city!="" and (city[-1] == "市") and random.random() < 0.3:
            city = city[0:-1]
        if province in direct_city:
            province = ""
        comp_str = "".join((province, city, self.country, self.town, self.detail_address))
        insert_point = random.randint(0, len(comp_str))
        while not check_insert_point(comp_str, insert_point): insert_point = random.randint(0, len(comp_str))
        comp_str = comp_str[0:insert_point] + self.phone + comp_str[insert_point:len(comp_str)]
        comp_str = "%s,%s." % (self.name, comp_str)
        return comp_str

class EntryVar2(Base):
    __tablename__ = 'entry2'
    _id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("guest_address._id"))
    parent = relationship("GuestAddress")
    name = Column(String(6))
    phone = Column(String(12))
    province = Column(String(12))
    city = Column(String(12))
    country = Column(String(12))
    town = Column(String(12))
    road = Column(String(64))
    house_number = Column(String(64))
    detail_address = Column(String(256))
    composed_string = Column(String(1024))

    def compose_string(self) -> str:
        province = self.province
        city = self.city
        if (province[-1] == "省") and random.random() < 0.3:
            province = province[0:-1]
        if city !="" and (city[-1] == "市") and random.random() < 0.3:
            city = city[0:-1]
        if province in direct_city:
            province = ""
        comp_str = "".join((province, city, self.country, self.town, self.road, self.house_number, self.detail_address))
        insert_point = random.randint(0, len(comp_str))
        while not check_insert_point(comp_str, insert_point): insert_point = random.randint(0, len(comp_str))
        comp_str = comp_str[0:insert_point] + self.phone + comp_str[insert_point:len(comp_str)]
        comp_str = "%s,%s." % (self.name, comp_str)
        return comp_str

class EntryVar3(Base):
    __tablename__ = 'entry3'
    _id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("guest_address._id"))
    parent = relationship("GuestAddress")
    name = Column(String(6))
    phone = Column(String(12))
    province = Column(String(12))
    city = Column(String(12))
    country = Column(String(12))
    town = Column(String(12))
    road = Column(String(64))
    house_number = Column(String(64))
    detail_address = Column(String(256))
    composed_string = Column(String(1024))

    def compose_string(self) -> str:
        addr = [self.province, self.city, self.country, self.town]

        if (addr[0][-1] == "省") and random.random() < 0.3:
            addr[0] = addr[0][0:-1]
        if addr[1] !="" and (addr[1][-1] == "市") and random.random() < 0.3:
            addr[1] = addr[1][0:-1]
        if addr[0] in direct_city:
            addr[0] = ""
        i = random.choice(range(0,4))
        while (addr[i]==""): i = random.choice(range(0,4))
        addr[i]=""
        if (random.random()<0.1) :
            while (addr[i] == ""): i = random.choice(range(0, 4))
            addr[i]=""
        comp_str = "".join((addr[0], addr[1], addr[2], addr[3], self.road, self.house_number, self.detail_address))
        insert_point = random.randint(0, len(comp_str))
        while not check_insert_point(comp_str, insert_point): insert_point = random.randint(0, len(comp_str))
        comp_str = comp_str[0:insert_point] + self.phone + comp_str[insert_point:len(comp_str)]
        comp_str = "%s,%s." % (self.name, comp_str)
        return comp_str

engine = sqlalchemy.create_engine('Sensitive Information Reducted')
DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
session = DBSession()