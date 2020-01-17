# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 09:16:45 2019

@author: pepo
"""

import libardrone
#import pygame
from time import sleep
import time
import cv2
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from threading import Thread
import os

import math
from shapely.geometry import LineString
from shapely.geometry import Point
from bluepy.btle import DefaultDelegate, Peripheral, Scanner 
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

debug=True

drone = libardrone.ARDrone()
ds_test = pd.DataFrame()
ds_oper = pd.DataFrame()
p = Point(0,0)
running = True

route={'p0':Point(0,0),'p1':Point(1,0),'p2':Point(1,1)}

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
    if debug:
        print("Intersection 0/1")
        print(result)
        print("Intersection 0/2")
        print(result2)
        print("Intersection 1/2")
        print(result3)
        time.sleep(5)
    point=None
    if len(result) > 0:
        if len(result2) > 0:
            message="case A: Circle 0&1 & 0&2 intersect"
            point_int=line_intersection([(result[0],result[1]), (result[2],result[3])], [(result2[0],result2[1]), (result2[2],result2[3])])
            point=Point(point_int[0],point_int[1])
        elif len(result3) > 0:
            message="case B: Circle 0&1 & 1&2  intersect"
            point_int=line_intersection([(result[0],result[1]), (result[2],result[3])], [(result3[0],result3[1]), (result3[2],result3[3])])
            point=Point(point_int[0],point_int[1])
        else:
            message="case G: Circle 0&1 intersect"
            point=Point((result[0]+result[2])/2,(result[1]+result[3])/2)
    elif len(result3) > 0 and len(result2) > 0:
        message="case C: Circle 0&1 & 1&2 intersect"
        point_int=line_intersection([(result2[0],result2[1]), (result2[2],result2[3])], [(result3[0],result3[1]), (result3[2],result3[3])])
        point=Point(point_int[0],point_int[1])
    elif len(result3) > 0:
        message="case D: Circle 1&2 intersect: Medium point"
        point=Point((result3[0]+result3[2])/2,(result3[1]+result3[3])/2)
    elif len(result2) > 0:
        message="case E: Circle 0&2 intersect: Medium point"
        point=Point((result2[0]+result2[2])/2,(result2[1]+result2[3])/2)
    else:
        message="case F: No intersection ERROR no signal"
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
    if debug:
        print(message)
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

def inverse(x):
    return x*(-1)

def get_current_position():
    MIN=30
    MAX=100
    SCALE=1.3
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(1.9)
    devlist=['30:ae:a4:9c:e7:c2','30:ae:a4:97:6c:26','30:ae:a4:9c:8f:a2']
    global ds_test
    for dev in devices:
            if dev.addr in devlist:
             #   print("ADDR: %s" % (dev.addr))
                data = [[time.time(),dev.addr,-1*dev.rssi,dev.iface,dev.addrType,dev.getValueText(1),dev.getValueText(10),dev.getValueText(255)]]
                #data = [[time.time()]]           
                ds_test=ds_test.append(data)
               
                #print("bucle: %d" % len(ds_test))
                
    if len(ds_test) == 0:
        return None
 #   else:
 #       print("bucle: %d" % (len(ds_test[ds_test[2]>=MIN])))
 #       print("bucle2: %d" % len(ds_test))
 #       return None
    
   
    
    
    ds_test=ds_test[ds_test[2]>=MIN]
    
    if debug:
        print("bucle2: %d" % len(ds_test))
        print(len(ds_test[ds_test[0]-(time.time())<2000]))
    #ds_test["rssi_norm"]=MAX-ds_test[2]
    ds_test["rssi_norm"]=(ds_test[2]-MIN)/(MAX-MIN)
    #ds_test["rssi_norm"]=1-ds_test["rssi_norm"]
    
    ds_test["rssi_norm"]=ds_test["rssi_norm"]*SCALE
    
    
    ds_test_b3=ds_test[ds_test[1]=="30:ae:a4:97:6c:26"] # 3 
    ds_test_b1=ds_test[ds_test[1]=="30:ae:a4:9c:e7:c2"] # 1
    ds_test_b2=ds_test[ds_test[1]=="30:ae:a4:9c:8f:a2"] # 2
    
 
    ds_b1 = 0
    ds_b2 = 0
    ds_b3 = 0

    if len(ds_test_b1) > 0 and time.time()-ds_test_b1.iloc[-1][0] < 10:
        ds_b1 = ds_test_b1.iloc[-1]["rssi_norm"]
            
    if len(ds_test_b2) > 0 and time.time()-ds_test_b2.iloc[-1][0] < 10:
        ds_b2 = ds_test_b2.iloc[-1]["rssi_norm"]

    if len(ds_test_b3) > 0 and time.time()-ds_test_b3.iloc[-1][0] < 10 :
        ds_b3 = ds_test_b3.iloc[-1]["rssi_norm"]

           
    print("Beacon 1:  %s" % (ds_b1))
    print("Beacon 2:  %s" % (ds_b2))
    print("Beacon 3:  %s" % (ds_b3))
    if debug:
        print("Summary:")
        print("#########")
        print("len ds_test %d" % (len(ds_test)))
        print(ds_b1)
        print(ds_b2)
        print(ds_b3)
        print("#########")
        print("Position 1:  %s" % (ds_b1))
        print("Position 2:  %s" % (ds_b2))
        print("Position 3:  %s" % (ds_b3))
        
        
    point=returnpoint(0,0,ds_b1,0,1,ds_b2,1,0.5,ds_b3)
    
    if point == None:
        point = Point(0,0)
        
    data = [[time.time()*1000,str(point.x),str(point.y),0,0,ds_b1,0,1,ds_b2,1,0.5,ds_b3]]        
    temp = pd.DataFrame(data)        
    temp.to_csv('/home/pepo/Documents/nissan_code/Loc_csv.csv',mode='a', header=False)        
        
    return point


def get_info():
    print('Battery %i%%' % drone.navdata.get(0,dict()).get('battery',0))
    print('State %i' % drone.navdata.get(0,dict()).get('ctrl_state',0))
    print('Theta %i' % drone.navdata.get(0,dict()).get('theta',0))
    print('Phi %i' % drone.navdata.get(0,dict()).get('phi',0))
    print('PSI %i' % drone.navdata.get(0,dict()).get('psi',0))
    print('Altitude %i' % drone.navdata.get(0,dict()).get('altitude',0))
    print('vx %i' % drone.navdata.get(0,dict()).get('vx',0))
    print('vy %i' % drone.navdata.get(0,dict()).get('vy',0))
    print('vz %i' % drone.navdata.get(0,dict()).get('vz',0))

def get_detail(name):
    return drone.navdata.get(0,dict()).get(name,0)

def takeoff(height):
    drone.takeoff()
    
def move_left(secs):
    drone.move_left()
    sleep(secs)

def move_right(secs):
    drone.move_right()
    sleep(secs)

def turn_right(secs):
    drone.turn_right()
    sleep(secs)

def turn_left(secs):
    drone.turn_left()
    sleep(secs)
    
def move_ff(secs):
    drone.move_forward()
    sleep(secs)
        
def move_back(secs):
    drone.move_backward()
    sleep(secs)
        
def move_up(secs):
    drone.move_up()
    sleep(secs)
        
def move_down(secs):
    drone.move_down()
    sleep(secs)    


def threadlocation(threadname):
    global p
    global running
    while running:
        p = get_current_position()
        if debug:
            print(p)
        if p == None:
            p = Point(0,0)
    os._exit(0)




def main():
    global running
    cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
    #drone = libardrone.ARDrone()
    drone.takeoff()
    while running:
    # get current frame of video
        running, frame = cam.read()
        str_image = ("Location: X(%s) , Y(%s) \n Battery: %s \n Height: %s" % (str(round(p.x,2)),str(round(p.y,2)),str(get_detail('battery')),str(get_detail('altitude'))))
        font=cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,str_image,(0,30),font,0.5,(0,255,0),1,cv2.LINE_AA,bottomLeftOrigin=False)
        #print(get_current_position())
        if running:
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == 27: 
            # escape key pressed
                running = False
                print("Exit requested")
                
        else:
        # error reading frame
            print ('error reading video feed')
    drone.land()
    cam.release()
    cv2.destroyAllWindows()
    os._exit(0)



def inittrack():
    THRESHOLD=0.002
    global p
    global ds_oper
    items=len(route)
    i=0
    while i<items:
        name = 'p'+str(i)
        target = route[name]
        print("Situation")
        print("Target X: %s Y: %s" % (str(target.x),str(target.y)))
        print("Position X: %s Y: %s" % (str(p.x),str(p.y)))
        print("Distance:")
        print("X: %s Y: %s" % (str(p.x-target.x),str(p.y-target.y)))
        a=p.x-target.x
        b=p.y-target.y
 
        op=""
        if abs(a)<THRESHOLD and abs(b)<THRESHOLD:
            i=i+1
            print("point found")
        if a>0:
            op=op+"B"
            print("move backwards")   
        else:
            op=op+"F"
            print("move forwards")
        if b<0:
            op=op+"R"
            print("move right")
        else:
            op=op+"L"
            print("move left")
        data = [[time.time()*1000,str(target.x),str(target.y),str(p.x),str(p.y),op]]        
        temp = pd.DataFrame(data)        
  #      temp.to_csv('/home/pepo/Documents/nissan_code/Loc_csv.csv',mode='a', header=False)        
        time.sleep(2)
    

if __name__ == '__main__':
    try:    
        drone.trim()
        drone.speed = 0.2
        if False:
            thread_loc = Thread(target=threadlocation, args=['t1'])
            thread_loc.start()
        if False:
            thread_main = Thread(target=main, args=[])
            thread_main.start()
       # inittrack()
        print("take off")
        drone.takeoff()
        sleep(5)
        print("move up")        
        drone.move_up()        
        sleep(5)      
        print("move left")
        drone.move_left()
        sleep(3)
        print("hover")
        drone.hover()
        sleep(1)
        print("move down")
        drone.move_down()
        sleep(5)
        print("move right")
        drone.move_right()
        sleep(3)
        print("hover")
        drone.hover()
        sleep(1)
        
    #    sleep(1)
        
        
        print("land")
        drone.land()
    except (SystemExit,KeyboardInterrupt):
        drone.land()
        drone.halt()
        print("Dron Aborted")
    except:
        drone.land()
        drone.halt()
        print("Dron Exception Aborted")
    drone.halt()