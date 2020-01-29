# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""




import numpy as np
import pandas as pd
import drone 
import applogger as log

import location
from  location import beacon

locations = {}




locations[0]=beacon(0,0,"fd:aa:ec:36:8b:66")
locations[1]=beacon(1,0,"d0:93:86:c0:de:bd")
locations[2]=beacon(1,1,"ef:40:e0:1a:5d:7f")
locations[3]=beacon(0,1,"id3")

actual = 0

drone.init()
while actual < len(locations)-1:
    
    currentpos=location.getposition(locations)
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
    
    
    actual = 10







