# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""




import numpy as np
import pandas as pd
#import drone 
import applogger as log

import location
from  location import beacon


#global locations
locations = {}



locations[0]=beacon(0,0,"d0:93:86:c0:de:bd")
locations[1]=beacon(1,0,"ef:40:e0:1a:5d:7f")
locations[2]=beacon(0,1,"fd:aa:ec:36:8b:66")
locations[3]=beacon(1,1,"ec:a6:9d:22:1c:1f")

actual = 0

#drone.init()
while actual < len(locations)-1:
    
    tests = {}
    tests[0]=location.unittest(locations,0,0,-41,-79,-92,-84)    
    tests[1]=location.unittest(locations,0.33,0,-77,-77,-90,-92)    
    '''     
    tests[2]=location.unittest(locations,0.66,0,-85,-60,-90,-82)    
    tests[3]=location.unittest(locations,1,0,-87,-35,-91,-86)    
    print(type(tests))    
    
    
    location.unittest(locations,0,0.33,-76,-76,-76,-79)    
    location.unittest(locations,0.33,0.33,-85,-85,-74,-77)
    location.unittest(locations,0.66,0.33,-89,-66,-83,-81)
    location.unittest(locations,1,0.33,-90,-66,-77,-86)
    
    location.unittest(locations,0,0.66,b1,b2,b3,b4)    
    location.unittest(locations,0.33,0.66,b1,b2,b3,b4)    
    location.unittest(locations,0.66,0.66,b1,b2,b3,b4)    
    location.unittest(locations,1,0.66,b1,b2,b3,b4)     
    
    location.unittest(locations,0,1,b1,b2,b3,b4)    
    location.unittest(locations,0.33,1,b1,b2,b3,b4)    
    location.unittest(locations,0.66,1,b1,b2,b3,b4)    
    location.unittest(locations,1,1,b1,b2,b3,b4)    
   
        
    currentpos=location.getposition(locations)
    if currentpos.x + currentpos.y > 0 :    
        distance=location.getdistance(currentpos,locations[actual])
        action=location.getaction(distance)
        if action == location.FOUND:
            log.log(log.INFO,"Location %s of id %s Found" % (actual,locations[actual].id))
            log.log(log.INFO,"Start scan")
            drone.scan()
            log.log(log.INFO,"Scan completed")
            actual=actual+1
            log.log(log.INFO,"Target Updated")
        else:
            log.log(log.INFO,"Perform Actions: START")
            drone.perform(action)
            log.log(log.INFO,"Perform Actions: END")
    else:
        log.log(log.ERROR,"Trilateration Fail")
    
    '''

    actual = 10





