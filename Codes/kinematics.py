#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 09:13:44 2021

@author: amanda
"""


'''
This code contains classes for kinematic operations
'''

import numpy as np
import math as m

Rotary = 0
Prismatic = 1

class DHMatrix :   
    
    '''
    This is Denavit-Hartenberg matrix
    '''
    
    def __init__ (self, pa=0.0, palfa=0.0, pd=0.0, ptheta=0.0, ptype=Rotary):
        
        
        self._a = pa
        self._alfa = m.radians(palfa)
        self._theta = m.radians(ptheta)
        self._type = ptype
        self._mat = np.eye(4)
        self._mat[0,0] = self._mat[1,1] = m.cos(self._theta)
        self._mat[1,0] = m.sin(self._theta)
        self._mat[0,1] = -self._mat[1,0] 
        self._mat[2,0] = self._mat[2,1] = self._mat[3,0] = self._mat[3,1] = self._mat[3,2] = 0.0                        
        self._mat[3,3] = 1.0
        self._mat[2,3] = pd
        s_alfa= m.sin(self._alfa)
        self._mat[0,2] = s_alfa * self._mat[1,0]
        self._mat[1,2] = -s_alfa * self._mat[0,0]
        self._mat[0,3] = self._a * self._mat[0,0]
        self._mat[1,3] = self._a * self._mat[1,0]
        self._mat[2,2] = m.cos(self._alfa)
        
    def update(self, q): 
        
        '''
        This method updates matrix's values 
        '''
        
        if self._type == Prismatic:
            self._mat[2][3] = q
        else:
            self._theta = q
            self._mat[0][0] = self._mat[1][1] = m.cos(q)
            self._mat[1][0] = m.sin(q)
            self._mat[0][1] = -self._mat[1,0]
            self._mat[0][3] = self._a * m.cos(q)
            self._mat[1][3] = self._a * m.sin(q)
            
    def __mul__ (self, element):
        
        '''
        This method defines how to multiply a DHMatrix
        '''
        
        result = DHMatrix()        
        result._mat = np.dot(self._mat, element._mat)
        return result

class Joint:

    '''
    This is a joint 
    '''    
    
    def __init__ (self, j_type = Rotary, theta = 0.0, d = 0.0):
        
        '''
        j_type: joint can be rotary or prismatic 
        theta: joint angle
        d: 
        '''
        
        self.moved = False
        self.type = j_type
        self.theta = theta
        self.d = d
        self.value = self.theta if self.type == Rotary else self.d  
        
    def moveJoint (self, angle):
        
        '''
        This method moves joint to (current angle + angle)
        '''
        self.value = angle
        if self.type == Rotary:
            self.theta += angle
            if self.theta > self.max:
                self.theta = self.max
            if self.theta < self.min:
                self.theta = self.min           
        else:
            self.d += angle
            if self.d > self.max:
                self.d = self.max
            if self.d < self.min:
                self.d = self.min
                
        self.moved = True    

    @property
    def value(self):
        
        '''
        This method returns theta for rotary joints and d for prismatic joints
        '''
        
        if self.type == Rotary:
            return self.theta
        else:
            return self.d   
           
    @value.setter
    def value (self, value):
        
        '''
        This method moves joint to angle
        '''
        self._value = value
        if self.type == Rotary:
            self.theta = value
        else:
            self.d = value
        self.moved = True  
              
class Link: 
    
    '''
    This is a link 
    '''
    
    def __init__ (self, length = 1.0):
                
        self.length = length
        
class KinematicChain:
    
    '''
    This is a kinematic chain that represents a robotic arm
    '''
    
    def __init__ (self):
        
        
        self.joints = []
        self.links= []                
        self.matrizes = []
    
    def add_joints (self, *args):
        
        '''
        This method appends joint(s) to self.joints
        '''
        
        for j in args:
            self.joints.append(j)

        
    def add_links (self, *args):
        
        '''
        This method appends link(s) to self.links
        '''
        
        for e in args:
            self.links.append(e)        
        
    def calcDHMatrix (self):
        
        '''
        Forward Kinematics
        This method determines the x, y, z coordinates of each joint 
        '''

        mul = DHMatrix(0)
        self.x, self.y, self.z = [mul._mat[0][3]], [mul._mat[1][3]], [mul._mat[2][3]]
        for i in range(len(self.matrizes)):            
            mul=  mul * self.matrizes[i]
            self.x.append(round(mul._mat[0][3],3))
            self.y.append(round(mul._mat[1][3],3))
            self.z.append(round(mul._mat[2][3],3))
          
    def create (self): 
        
        '''
        This method creates DHMatrix objects for each joint and
        calculates forward kinematics
        '''
        
        for i in range(len(self.links)):
            e= (self.links[i]).length
            d= (self.joints[i]).d
            t= (self.joints[i]).theta
            j_type = (self.joints[i]).type
            self.matrizes.append(DHMatrix(e, 0, d, t, j_type))   
            
        self.calcDHMatrix()   
        return [self.x[-1], self.y[-1], self.z[-1]]         
        
    def update (self):
        
        '''
        This method updates DHMatrix objects for each joint that has been
        moved and calculates forward kinematics
        '''

        for i in range(len(self.matrizes)):
            if self.joints[i].moved:      
                self.matrizes[i].update(
                        self.joints[i].d if self.joints[i].type 
                        else m.radians(self.joints[i].theta))
                self.joints[i].moved = False
                
        self.calcDHMatrix()
    
    def inverse(self, coordinates):
        
        '''
        Inverse kinematics
        This method determines the best joint values to reach the desired
        coordinates (x, y, z)
        '''
        
        x,y,z= coordinates
        l1 = self.links[1].length
        l2 = self.links[2].length
        options = np.ones((2,2))
        options[1, 0] =  m.acos((x**2 + y**2 - l2**2 - l1**2 )/(2*l1 * l2))
        options[1, 1] = - options[1, 0]
        
        for i in range(2):
            q = options[1, i]
            options[0, i] =  m.atan2(l2 * m.sin(q) * x + (l1 + l2 * m.cos(q)) * y,
                                    (l1 + l2 * m.cos(q)) * x - l2 * m.sin(q) * y) 
            
        options[1, :] = - options[1, :]
        values = [z - self.joints[3].d] + [m.degrees(q) for q in options[:, np.absolute(options).sum(axis=0).argmin()]] + [self.joints[3].value]
        return values
        

if __name__ == "__main__":
    
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from time import time
    import random
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')  
    plt.ion()
    
    def plot(kin_chain):
        ax.lines = []     
        pl, = ax.plot(kin_chain.x, kin_chain.y, kin_chain.z,'cs-' , markersize=7)  
        plt.show(block = False)   
        plt.pause(1)
        
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_xlim([0,0.4])
    ax.set_ylim([-0.4,0.4])
    ax.set_zlim([0,0.4])
    ax.set_xticks(list(np.linspace(0,0.4,6)))
    ax.set_yticks(list(np.linspace(-0.4,0.4,6)))
    ax.set_zticks(list(np.linspace(0,0.4,6)))
    t0 = time()
    kin_chain = KinematicChain()
    j0 = Joint(Prismatic, d=0.4)
    j1 = Joint()
    j2 = Joint()
    j3 = Joint(d = -0.2)
    kin_chain.add_joints(j0, j1, j2, j3)
    kin_chain.add_links(Link(0), Link(0.2), Link(0.2), Link(0))
    kin_chain.create()    
    plot(kin_chain)
    
    values = kin_chain.inverse([0.105, -0.03, 0.0])
    kin_chain.joints[0].value = values[0]
    kin_chain.joints[1].value = values[1]
    kin_chain.joints[2].value = values[2]
    kin_chain.joints[3].value = values[3]
    kin_chain.update()
    plot(kin_chain)

    
   