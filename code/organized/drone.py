# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 16:34:39 2020

@author: PONO
"""

import location
import applogger as log
import time
'''
import olympe
from olympe.messages.ardrone3.Piloting import TakeOff

drone = olympe.Drone("10.202.0.1")
drone.connection()
drone(TakeOff()).wait()
drone.disconnection()
'''

def perform(operation):
    for action in operation:
        if action==location.UP:
            log.log(log.INFO,"Action sent: UP")
            
        if action==location.DOWN:
            log.log(log.INFO,"Action sent: DOWN")
            
        if action==location.LEFT:
            log.log(log.INFO,"Action sent: LEFT")
            
        if action==location.RIGHT:
            log.log(log.INFO,"Action sent: RIGHT")
            
        if action==location.FORWARD:
            log.log(log.INFO,"Action sent: FWD")
            
        if action==location.BACKWARD:
            log.log(log.INFO,"Action sent: BACKWARD")
            
    return


def evalpicture(image):
    t1 = time.time()
    log.log(log.INFO,"Image Sent for Evaluation")
    
    # Invoke models
    
    t2 = time.time()
    log.log(log.INFO,"Image Evaluated")
    log.timer("Image Evaluated",t2-t1)
    
    return


def scan():
    
    return

def init():
    
    return