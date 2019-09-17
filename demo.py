import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy import and_
from api import guess
from sqlalchemy.sql import func
from sqlalchemy.orm import load_only
import atexit
import re
import random
import json
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from model import *


from typing import *
example=[]
example2: List[EntryVar2] = []


def update():
    example.clear()
    example2.clear()
    for i in range(2):
        entry = session.query(Entry).order_by(func.random()).first()
        example.append(entry)
    entry2: EntryVar2 = session.query(EntryVar2).order_by(func.random()).first()
    example2.append(entry2)

sched = BackgroundScheduler(daemon=True)
sched.add_job(update,"interval", hours=4)
sched.start()
atexit.register(lambda : sched.shutdown())
app=Flask(__name__)

def format(entries, e2):
    r=[]
    for entry in entries:
        r.append({
            "input": entry.compose_string(),
            "answer": {
                "姓名": entry.name,
                "手机": entry.phone,
                "地址": [
                    entry.province, entry.city, entry.country, entry.town, entry.detail_address
                ]
            }
        })
    for entry2 in e2:
        r.append({
            "input": entry2.compose_string(),
            "answer": {
                "姓名": entry2.name,
                "手机": entry2.phone,
                "地址": [
                    entry2.province, entry2.city, entry2.country, entry2.town, entry2.road, entry2.house_number, entry2.detail_address
                ]
            }
        })
    return r
from flask import jsonify
@app.route("/test")
def a():
    r = format(example, example2)
    return jsonify(r)

def main():
    app.config['JSON_AS_ASCII']= False
    update()
    app.run(host="0.0.0.0", port=10223)
    pass

if __name__=='__main__':
    main()