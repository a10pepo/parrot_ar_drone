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




def unittest(locations,x,y,b1,b2,b3,b4):
    global lastlocation
    global ds_test
    print("TEST START")
    
    data = [[time.time()*1000,locations[0].getid(),b1,"","","","","",locations[0].x,locations[0].y]]
    ds_test=ds_test.append(data)
    data = [[time.time()*1000,locations[1].getid(),b2,"","","","","",locations[1].x,locations[1].y]]
    ds_test=ds_test.append(data)
    data = [[time.time()*1000,locations[2].getid(),b3,"","","","","",locations[2].x,locations[2].y]]
    ds_test=ds_test.append(data)
    data = [[time.time()*1000,locations[3].getid(),b4,"","","","","",locations[3].x,locations[3].y]]
    ds_test=ds_test.append(data)
    
    point=executepoint(ds_test,locations)
    ds_test=ds_test.iloc[0:0]
    lastlocation=position(0.3555, 0.28111)
    distance = getdistance(point,Point(x,y))
    print("Punto: (%s,%s) --> (%s,%s)  : distance:  %s" % (x,y,point.x,point.y,distance))
    print("TEST END")
    return distance

def getposition(locations):   
    global lastlocation
    global ds_test
    
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(4)
    
    dispids= []
    for i in range(0,len(locations)):
        dispids.append(locations[i].getid())
   
    for dev in devices:
           
            if dev.addr in dispids:
                for loc in range(0,len(locations)):
                    if locations[loc].getid() == dev.addr:
                        data = [[time.time()*1000,dev.addr,dev.rssi,dev.iface,dev.addrType,dev.getValueText(1),dev.getValueText(10),dev.getValueText(255),locations[loc].x,locations[loc].y]]
                        ds_test=ds_test.append(data)
                
    
    
    
    
    point=executepoint(ds_test,locations)
                
    lastlocation=position(point.x,point.y)
    log.log(log.INFO,"Location Updated")
    return lastlocation

def getdistance(position,target):
    x = position.x - target.x 
    y = position.y - target.y 
    
    return (x,y)
    
def getdistancemeassure(position,target):
    dist=math.sqrt((position.x - target.x)**2+(position.y - target.y)**2)
    return dist

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
    print("Intersection: (%s , %s)" % (x,y))
    return x, y



def setble(x,y,radius,clr):
    return plt.Circle((x,y),radius,fc="none",edgecolor=clr)

def returnpoint(x0,y0,r0,x1,y1,r1,x2,y2,r2):
    result=calculateintersection(x0,y0,r0,x1,y1,r1)
    result2=calculateintersection(x0,y0,r0,x2,y2,r2)
    result3=calculateintersection(x1,y1,r1,x2,y2,r2)
    '''
    print("Intersection 1/2")
    print(result)
    print("Intersection 1/3")
    print(result2)
    print("Intersection 2/3")
    print(result3)
    '''
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
            point=Point(-1,-1)
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
        point=Point(-1,-1)
    #x = np.linspace(0, 1, 100000)
    
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.grid(linestyle='--')
    ax.set_aspect(1)
    ax.add_artist(setble(x0,y0,r0,"r")) # Beacon1
    ax.add_artist(setble(x1,y1,r1,"g")) # Beacon2
    ax.add_artist(setble(x2,y2,r2,"b")) # Beacon3
    if len(result) >0:
        ax.add_artist(setble(result[0],result[1],0.001,"b")) 
        ax.add_artist(setble(result[2],result[3],0.001,"b")) 
    if len(result2) >0:
        ax.add_artist(setble(result2[0],result2[1],0.001,"b")) 
        ax.add_artist(setble(result2[2],result2[3],0.001,"b")) 
    if len(result3) >0:
        ax.add_artist(setble(result3[0],result3[1],0.001,"b")) 
        ax.add_artist(setble(result3[2],result3[3],0.001,"b")) 
    ax.add_artist(setble(point.x,point.y,0.01,"r"))
    
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
   # print("Point 1 %s , %s" % (intersectionPoint1_x,intersectionPoint1_y ))
   # print("Point 2 %s , %s" % (intersectionPoint2_x,intersectionPoint2_y ))
    
    
    return [intersectionPoint1_x,intersectionPoint1_y,intersectionPoint2_x,intersectionPoint2_y]


def executepoint(ds_test,locations):
    MIN=30
    MAX=100
    
    

    
    # Get TOP 3 for triangulation       
    ds_test=ds_test.sort_values(by=[2],ascending=False)
    ds_test=ds_test[:3]

    ds_test[2]=ds_test[2]*-1
    ds_test=ds_test[ds_test[2]>=MIN]

#    ds_test["rssi_norm"]=MAX-ds_test[2]
    #ds_test["rssi_norm"]=ds_test["rssi_norm"]*1.7   
    #ds_test["rssi_norm"]=(ds_test[2]-MIN)/(MAX-MIN)
#    ds_test["rssi_norm"]=(ds_test[2]-(1/MAX))/((1/MIN)-(1/MAX))
    ds_test["rssi_norm"]=ds_test[2]/100
    # This inversion allows you to use small rssi     
    #ds_test["rssi_norm"]=1-ds_test["rssi_norm"]
    
    
    ds_test["rssi_norm"]=ds_test["rssi_norm"]
     
    ds_test_b1=ds_test.iloc[-1]# 1
    ds_test_b2=ds_test.iloc[-2] # 2
    ds_test_b3=ds_test.iloc[-3] # 3
    
   
    
        
    
    print("Summary:")

    
    print("#########")
    print("Position 0: %s,%s %s RSSI: %s" % (ds_test_b1[8],ds_test_b1[9],ds_test_b1["rssi_norm"],ds_test_b1[2]))
    print("Position 1: %s,%s %s RSSI: %s" % (ds_test_b2[8],ds_test_b2[9],ds_test_b2["rssi_norm"],ds_test_b2[2]))
    print("Position 2: %s,%s %s RSSI: %s" % (ds_test_b3[8],ds_test_b3[9],ds_test_b3["rssi_norm"],ds_test_b3[2]))
    print("#########")
    
    
    
    point=returnpoint(ds_test_b1[8],ds_test_b1[9],ds_test_b1["rssi_norm"],ds_test_b2[8],ds_test_b2[9],ds_test_b2["rssi_norm"],ds_test_b3[8],ds_test_b3[9],ds_test_b3["rssi_norm"])
    print(point)
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



