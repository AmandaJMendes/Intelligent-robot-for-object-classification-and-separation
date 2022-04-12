
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Apr 14 13:59:26 2021

@author: amanda
"""

from kinematics import Joint, Link, KinematicChain, Rotary, Prismatic
from motion_planning import PolyTrajectory, Path
from image import ObjectDetector
from classification import ImageClassifier 
import json
import serial



class RISO (KinematicChain, ObjectDetector, ImageClassifier):
    
    '''
    This class contains methods for operating RISO
    '''
    
    def __init__ (self, img_shape, model, classes, real_x = 0.3, real_y = 0.3, serial_port = '/dev/ttyS0', serial_baudrate = 9600):
        
        '''
        This constructor:
            Initializes KinematicChain, ObjectDetector and ImageClassifier objects
            Opens serial connection with ESP32
        '''
        
        KinematicChain.__init__(self)
        ObjectDetector.__init__(self, img_shape, real_x, real_y)
        ImageClassifier.__init__(self, img_shape, model, classes)
        self.serial = serial.Serial(serial_port, serial_baudrate)
        
    def configKinChain (self):
        
        '''
        This method adds RISO's elements to kinematic chain 
        '''
        
        self.add_joints(Joint(Prismatic, d=0.4), Joint(), Joint(), Joint(d=-0.2))
        self.add_links(Link(0), Link(0.2), Link(0.2), Link(0))
        self.create()
        
    def configRobot (self):
        
        '''
        This method sets RISO's initial position 
        '''
        #Move RISO até chaves de fim de curso
        self.move([0.0, 0.4, 0.2])
        #home = [0.4, 90.0, 0.0, 0.0]
        #for j in range(len(self.joints)):
        #        self.joints[j].value = home[j]
        #self.update()

    
    def move (self, destination):
        
        '''
        This method:
            Sends ESP32 instructions to move RISO to destination
            Moves KinematicChain's joints accordingly
        '''
        
        print ('Destination: {}.\n'.format(destination))
        joints_initial = [j.value for j in self.joints]
        try:
            joints_final = self.inverse(destination)
            
        except ValueError:
            return None
        path = Path(0, 5, joints_initial, joints_final)
        traj = PolyTrajectory(path, 1.0)
        traj.createPolynomials()
        for point in traj:
            #print (json.dumps({'initial':[round(i,3) for i in joints_initial], 'final': [round(i,3) for i in point[1][0]]}).encode('utf-8'))
            self.serial.write(json.dumps({'initial':[round(i,3) for i in joints_initial], 'final': [round(i,3) for i in point[1][0]]}).encode('utf-8'))
            ansr = self.serial.readline()
            joints_values = json.loads(ansr)['estimated']
            #joints_values = joints_final
            for j in range(len(self.joints)):
                self.joints[j].value = joints_values[j]
            self.update()
            joints_initial = [j.value for j in self.joints]
        return ((self.x[-1], self.y[-1], self.z[-1]))
        #print ('Position: {}.\n'.format((self.x[-1], self.y[-1], self.z[-1])))
        