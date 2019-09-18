import re
import random

def get_phone():
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
               "147", "150", "151", "152", "153", "155", "156", "157", "158", "159",
               "186", "187", "188", "189"]
    return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))

def check_insert_point(input,point):
    flag=True
    if point>0 and input[point-1].isdigit():
        flag=False
    if point<len(input) and input[point].isdigit():
        flag=False
    return flag

xing = None
ming = None

direct_city = ["北京","上海","天津","重庆"]


with open("xing.txt") as xing_file:
    line = xing_file.readline()
    xing = line.split(" ")
with open("ming.txt") as ming_file:
    line = ming_file.readline()
    ming = line.split(" ")

def get_name():
    a = random.choice(xing)
    b=""
    for i in range(random.randint(1,2)):
        b+=random.choice(ming)
    return a+b

def process_omit(entry):
    o=False
    if (entry.city == "") or (entry.country == "") or (entry.town == ""): o = True
    rand = random.random()
    if (not o) and (entry.province not in direct_city) and entry.country[-1]=="县":
        if random.random()<0.1:
            entry.city=""
    if (not o) and (rand<0.1):
        entry.town=""
        o=True
    rand = random.random()
    if (not o) and (entry.country[-1]=="区") and (rand<0.1):
        entry.country=""
        o=True
    return entry

def compose_string(entry):
    province = entry.province
    city = entry.city

    if (province[-1]=="省") and random.random()<0.3:
        province=province[0:-1]
    if (city[-1]=="市") and random.random()<0.3:
        city = city[0:-1]
    if province in direct_city:
        province=""
    comp_str = "".join((province, city, entry.country,entry.town, entry.detail_address))
    insert_point = random.randint(0,len(comp_str))
    while not check_insert_point(comp_str,insert_point): insert_point = random.randint(0,len(comp_str))
    comp_str = comp_str[0:insert_point]+entry.phone+comp_str[insert_point:len(comp_str)]
    comp_str = "%s,%s." % (entry.name, comp_str)
    return comp_str

pattern=re.compile(r"\d")
def qualifyGuessAddress(address):
    qualify=False
    if pattern.search(address) is not None:
        qualify=True
    if ("村" in address) and (address[-1:]!='村'):
        qualify=True
    return qualify