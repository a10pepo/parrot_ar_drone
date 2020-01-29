# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:07:06 2020

@author: PONO
"""


locations[0]=beacon(0,0,"id0")
locations[1]=beacon(1,0,"id1")
locations[2]=beacon(1,1,"id2")
locations[3]=beacon(0,1,"id3")





class beacon:
    
    def __init__(self,x,y,id):
        self.x=x
        self.y=y
        self.id=id
    
    def getid(self):
        return self.id
    
    def getcoordinates(self):
        return (self.x,self.y)