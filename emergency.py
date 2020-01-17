# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 18:19:15 2019

@author: pepo
"""

import libardrone
import pygame
from time import sleep
import time
import cv2

drone = libardrone.ARDrone()

def operation(sleep):
    t1 = time.time()
    t2=t1
    while t2-t1<sleep:
        drone.turn_left()
        t2=time.time()


def main():

   

    
    drone.land()


if __name__ == '__main__':
    main()