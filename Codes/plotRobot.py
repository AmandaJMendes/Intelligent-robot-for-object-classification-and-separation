#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 10:36:50 2021

@author: amanda
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from kinematics import *
from time import sleep

class SimulatedRISO:
    
    def __init__(self):

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_zlabel('z')
        self.ax.set_xlim([0,0.4])
        self.ax.set_ylim([-0.2,0.2])
        self.ax.set_zlim([0,0.4])
        self.ax.set_xticks(list(np.linspace(0,0.4,6)))
        self.ax.set_yticks(list(np.linspace(-0.2,0.2,6)))
        self.ax.set_zticks(list(np.linspace(0,0.4,6)))
        self.objs = None
        
    def plotObjects(self, *args):
        if self.objs:
            self.objs.remove()
        self.objs = self.ax.scatter(args[0], args[1], len(args[0])*[0], color = 'black', s =100)
        plt.show(block = False)
        plt.pause(0.5)
    
    def plotContainers(self, *args):
        
        self.ax.scatter(args[0], args[1], args[2], s = 400, marker = 's', color = (0.6, 0.0, 0.2) )
        plt.show(block = False)
        plt.pause(0.5)
        
    def plotRobot(self, kin_chain):
        self.ax.lines = []     
        pl, = self.ax.plot(kin_chain.x, kin_chain.y, kin_chain.z,'cs-' , markersize=12, linewidth = 4, markerfacecolor = 'black', color = (0.6, 0.0, 0.2))  
        plt.show(block = False)
        plt.pause(4)
        
if __name__ == '__main__':
    kin_chain = KinematicChain()
    j0 = Joint(Prismatic, d=0.4)
    j1 = Joint()
    j2 = Joint()
    j3 = Joint(d = -0.2)
    kin_chain.add_joints(j0, j1, j2, j3)
    kin_chain.add_links(Link(0), Link(0.2), Link(0.2), Link(0))
    kin_chain.create()    
    riso = SimulatedRISO()
    riso.plotObjects([0, 0.2, 0.4], [0.1, 0.0, -0.3])
    riso.plotContainers([0.2, 0.35], [0.35, 0.35], 2*[0.1])
    riso.plotRobot(kin_chain)   

