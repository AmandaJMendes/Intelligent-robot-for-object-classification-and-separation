#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 17:29:51 2021

@author: amanda
"""

import cv2
import numpy as np

class ObjectDetector:
    
    '''
    This is a class for object detection
    '''
    
    def __init__(self, img_shape, real_x, real_y):
        
        '''
        img_shape: e.g.: (480, 480, 3) - shape of output images
        '''
        self.i = 0
        self.img_shape = img_shape
        self.real_x = real_x
        self.real_y = real_y
        
    def openCamera (self):
        
        '''
        This method opens the camera
        '''
        
        self.camera = cv2.VideoCapture(0)

    
    def closeCamera (self):
        
        '''
        This method closes the camera
        '''
        
        self.camera.release()

    def realCoordinates (self, pix_x, pix_y):
        mult_x = self.real_x / 430
        mult_y = self.real_y / 430
        world_x = 0.3 - (pix_y * mult_x)
        world_y = (pix_x - 430/2) * -mult_y
        
        return (round(world_x, 3), round(world_y,3))       
    
    def detectObjects (self):
        
        '''
        This method:
            Captures image
            Detects objects 
            Returns:
                detected: list of tuples
                tuple = (object's image (as array),
                         object's x-coordinate,
                         object's y-coordinate)
        '''
        
        _, capture = self.camera.read()
        base = np.ones((3,3), np.uint8)
        capture = capture[25:455, 65:495]
        color = cv2.cvtColor(capture, cv2.COLOR_BGR2GRAY)
        blur  = cv2.GaussianBlur(color, (7, 7), 0)
        tresh = cv2.threshold(blur, 90, 255, cv2.THRESH_BINARY_INV) 
        erode = cv2.erode(tresh[1], base, iterations=1)
        img_cont = cv2.dilate(erode, base, iterations=4)        
        _, contours, familia = cv2.findContours(img_cont.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        lower = np.array([0, 0, 0])
        upper = np.array([97, 255, 104])
        hsv = cv2.cvtColor(capture, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        image = cv2.bitwise_and(capture, capture, mask= mask)
        cv2.imwrite('img.png'.format(self.i), image)
        back = np.zeros(self.img_shape, dtype=np.uint8) 
        back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)
        self.i+=1
        objs = []        
        height, width, depth = self.img_shape
        #i =0
        for cnt in contours:
            try:
                (x, y, w, h) = cv2.boundingRect(cnt) 
                img = cv2.cvtColor(image[y:y+h, x:x+w],cv2.COLOR_BGR2GRAY)
                #cv2.imwrite(f'oi{i}.png', img)
                img_h, img_w = img.shape            
                yoff = round((height - img_h)/2)
                xoff = round((width - img_w)/2)
                result = back.copy()
                result[yoff:yoff+h, xoff:xoff+w] = img
                obj_img = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
               # cv2.imwrite(f'alto{i}.png', obj_img)
                #i+=1
                arr = (np.asarray(obj_img).astype('float32')/255).reshape(1, height, width, depth)
                wx, wy = self.realCoordinates(x+(w/2), y+(h/2))
                objs.append((arr, wx, wy))
            except:
                pass        
        return (objs)

if __name__ == '__main__':
    
    from queue import Queue
    qObjs = Queue()
    img_shape = (200,200,3)    
    detector = ObjectDetector(img_shape, 0.3, 0.3)
    detector.openCamera()
    detected = detector.detectObjects()
    for obj in detected:
        
        qObjs.put(obj)
        print ('Objeto detectado em: ({}, {})'.format(obj[1], obj[2]))        
    detector.closeCamera()
