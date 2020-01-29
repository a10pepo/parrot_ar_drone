# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 11:58:35 2020

@author: PONO
"""

import applogger as log

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import math
from shapely.geometry import LineString
from shapely.geometry import Point
from bluepy.btle import DefaultDelegate, Peripheral, Scanner 
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
import time

UP="U"
DOWN="D"
LEFT="L"
RIGHT="R"
FORWARD="F"
BACKWARD="B"
FOUND="O"

THRESHOLD=0.1
ds_test = pd.DataFrame()
df_points = pd.DataFrame(columns=['time', 'x', 'y'])


def getposition(locations):   
    global lastlocation
    
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(4)
    
    dispids= []
    for i in range(0,len(locations)):
        dispids.append(locations[i].getid())
   
    for dev in devices:
            if dev.addr in dispids:
                data = [[time.time()*1000,dev.addr,dev.rssi,dev.iface,dev.addrType,dev.getValueText(1),dev.getValueText(10),dev.getValueText(255)]]
                ds_test=ds_test.append(data)
                
    point=executepoint(ds_test)
                
    lastlocation=position(0.3555, 0.28111)
    log.log(log.INFO,"Location Updated")
    return lastlocation

def getdistance(position,target):
    x = position.x - target.x 
    y = position.y - target.y 
    log.log(log.INFO,"Distance Calculated: x: %s  y: %s " % (x,y))
    return [x,y]

def getaction(distance):
    a = distance[0]
    b = distance[1]
    op=""
    if abs(a)<THRESHOLD and abs(b)<THRESHOLD:
            op="O"
    if a>0:
            op=op+"B"
    else:
            op=op+"F"
    if b<0:
            op=op+"R"
    else:
            op=op+"L"
    log.log(log.INFO,"Actions Calculated: %s" % (op))
    return op


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y



def setble(x,y,radius,clr):
    return plt.Circle((x,y),radius,fc="none",edgecolor=clr)

def returnpoint(x0,y0,r0,x1,y1,r1,x2,y2,r2):
    result=calculateintersection(x0,y0,r0,x1,y1,r1)
    result2=calculateintersection(x0,y0,r0,x2,y2,r2)
    result3=calculateintersection(x1,y1,r1,x2,y2,r2)
    """
    print("Intersection 0/1")
    print(result)
    print("Intersection 0/2")
    print(result2)
    print("Intersection 1/2")
    print(result3)
    """
    point=None
    if len(result) > 0:
        if len(result2) > 0:
            print("case A: Circle 1 and 2 intersect")
            point_int=line_intersection([(result[0],result[1]), (result[2],result[3])], [(result2[0],result2[1]), (result2[2],result2[3])])
            point=Point(point_int[0],point_int[1])
        elif len(result3) > 0:
            print("case B: Circle 1 and 3 intersect")
            point_int=line_intersection([(result[0],result[1]), (result[2],result[3])], [(result3[0],result3[1]), (result3[2],result3[3])])
            point=Point(point_int[0],point_int[1])
        else:
            print("case G: Circle 1 has no intersect: ERROR")
            point=Point(0,0)
    elif len(result3) > 0 and len(result2) > 0:
        print("case C: Circle 2 and 3 intersect")
        point_int=line_intersection([(result2[0],result2[1]), (result2[2],result2[3])], [(result3[0],result3[1]), (result3[2],result3[3])])
        point=Point(point_int[0],point_int[1])
    elif len(result3) > 0:
        print("case D: Circle 2 and 3 intersect: Medium point")
        point=Point((result3[0]+result3[2])/2,(result3[1]+result3[3])/2)
    elif len(result2) > 0:
        print("case E: Circle 1 and 3 intersect: Medium point")
        point=Point((result2[0]+result2[2])/2,(result2[1]+result2[3])/2)
    else:
        print("case F: No intersection ERROR no signal")
        point=Point(0,0)
    #x = np.linspace(0, 1, 100000)
    """fig, ax = plt.subplots(figsize=(12, 10))
    plt.grid(linestyle='--')
    ax.set_aspect(1)
    ax.add_artist(setble(x0,y0,r0,"r")) # Beacon1
    ax.add_artist(setble(x1,y1,r1,"g")) # Beacon2
    ax.add_artist(setble(x2,y2,r2,"b")) # Beacon3
    if len(result) >0:
        ax.add_artist(setble(result[0],result[1],0.01,"b")) # Samsung
        ax.add_artist(setble(result[2],result[3],0.01,"b")) # Samsung
    if len(result2) >0:
        ax.add_artist(setble(result2[0],result2[1],0.01,"b")) # Samsung
        ax.add_artist(setble(result2[2],result2[3],0.01,"b")) # Samsung
    if len(result3) >0:
        ax.add_artist(setble(result3[0],result3[1],0.01,"b")) # Samsung
        ax.add_artist(setble(result3[2],result3[3],0.01,"b")) # Samsung
    ax.add_artist(setble(point.x,point.y,0.01,"r"))
    """
    return point

def calculateintersection(x0,y0,r0,x1,y1,r1):
    EPSILON = 0.000001;
    dx = x1-x0
    dy = y1-y0
    d=math.sqrt((dy*dy)+(dx*dx))
    
    if d>r0+r1:
        return []
    
    if d < abs(r0-r1):
        return []
   
    a = ((r0*r0) - (r1*r1) + (d*d)) / (2.0 * d)
    point2_x = x0 + (dx * a/d)
    point2_y = y0 + (dy * a/d)
    h = math.sqrt((r0*r0) - (a*a))
    rx = -dy * (h/d)
    ry = dx * (h/d)
    
    
    intersectionPoint1_x = point2_x + rx
    intersectionPoint2_x = point2_x - rx
    intersectionPoint1_y = point2_y + ry
    intersectionPoint2_y = point2_y - ry

    return [intersectionPoint1_x,intersectionPoint1_y,intersectionPoint2_x,intersectionPoint2_y]


def executepoint(ds_test):
    MIN=30
    MAX=100
   

    ds_test[2]=ds_test[2]*-1
    ds_test=ds_test[ds_test[2]>=MIN]

    ds_test["rssi_norm"]=MAX-ds_test[2]
    ds_test["rssi_norm"]=(ds_test[2]-MIN)/(MAX-MIN)
    ds_test["rssi_norm"]=1-ds_test["rssi_norm"]
    
    ds_test["rssi_norm"]=ds_test["rssi_norm"]*1.1
    
    
    ds_test_b3=ds_test[ds_test[1]=="30:ae:a4:97:6c:26"] # 3 
    ds_test_b1=ds_test[ds_test[1]=="30:ae:a4:9c:e7:c2"] # 1
    ds_test_b2=ds_test[ds_test[1]=="30:ae:a4:9c:8f:a2"] # 2
    
 
    ds_b1 = 0
    ds_b2 = 0
    ds_b3 = 0

    if len(ds_test_b1) > 0:
        ds_b1 = ds_test_b1.iloc[-1]["rssi_norm"]
    if len(ds_test_b2) > 0:
        ds_b2 = ds_test_b2.iloc[-1]["rssi_norm"]
    if len(ds_test_b3) > 0:
        ds_b3 = ds_test_b3.iloc[-1]["rssi_norm"]
        
    """
    print("Summary:")
    print("#########")
    print(ds_b1)
    print(ds_b2)
    print(ds_b3)
    print("#########")
    print("Position 0: 0,0 %s" % (ds_b1))
    print("Position 1: 0,0 %s" % (ds_b2))
    print("Position 2: 0,0 %s" % (ds_b3))
    """    
    point=returnpoint(0,0,ds_b1,0,1,ds_b2,1,0.5,ds_b3)
    return point




class beacon:
    
    def __init__(self,x,y,id):
        self.x=x
        self.y=y
        self.id=id
    
    def getid(self):
        return self.id
    
    def getcoordinates(self):
        return (self.x,self.y)


class position:
    
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.timestamp=time.time()
        

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        """if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)
        """
    def handleNotification(self, cHandle, data):
        print(data)



