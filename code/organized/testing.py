# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 12:07:06 2020

@author: PONO
"""

from bluepy.btle import DefaultDelegate, Peripheral, Scanner 



 
 
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

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(4)
print(devices)