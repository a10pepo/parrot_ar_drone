# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 16:44:36 2020

@author: PONO
"""
import datetime
import time
import location
from elasticsearch import Elasticsearch
es = Elasticsearch()


DEBUG = "DEBUG"
INFO = "INFO"
ERROR= "ERROR"


def log(level,message):
    doc = {
    'level': level,
    'location': [location.lastlocation.x,location.lastlocation.y],
    'text': message,
    'timestamp': time.time()
    }
       
    if False:
        print(doc)
        

    #es.index(index="log-index", id=time.time(), body=doc)
        

def timer(message,time):
    doc = {
    'elapsedtime': time,
    'text': message,
    'timestamp': time.time()
    }
    #es.index(index="time-index", id=time.time(), body=doc)