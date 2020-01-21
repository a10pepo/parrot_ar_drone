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
    pygame.init()
    print(type(drone.image))
    print(drone.image)
    image = cv2.cvtColor(drone.image, cv2.COLOR_BGR2GRAY ) 
    # Displaying the image  
    cv2.imshow("test", image) 
    W, H = 320, 240
    screen = pygame.display.set_mode((W, H))
    print ("init")
    #drone = libardrone.ARDrone()
    print ("takeoff start")
    #drone.takeoff()
    #operation(2)
    
    #drone.land()
    print ("land end")
    pygame.quit()

if __name__ == '__main__':
    main()
