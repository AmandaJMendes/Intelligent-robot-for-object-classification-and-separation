#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 13:09:27 2021

@author: amanda
"""

"""
This is RISO's main code
"""
from riso import RISO
import numpy as np
from queue import Queue
from plotRobot import SimulatedRISO

model_dir = 'modeloNovo.tflite'
classes_dir = 'modelo.txt'
max_iter = 1
lim_prob = 90#Minimum probability accepted
containers = {'Porca': [0.05, 0.2, 0.1], 'Parafuso': [0.1, 0.2, 0.1], 'Undefined': [0.15, 0.2, 0.1]}
img_shape = (200,200,3)



print ('RISO is being initialized...\n')
riso = RISO(img_shape, model_dir, classes_dir)
riso.loadModel()
riso.loadClasses()
riso.configKinChain()
home = False

qClassObjs = Queue()
qObjs = Queue()


simul = SimulatedRISO()
plot_cont = np.array(list(containers.values()))
simul.plotContainers(plot_cont[:, 0], plot_cont[:, 1], plot_cont[:, 2])
simul.plotRobot(riso)   

for i in range(max_iter + 1):     
    
    if not home:
        print("RISO is moving to HOME.\n")
        riso.configRobot()
        simul.plotRobot(riso) 
        home = True
    
    riso.openCamera()
    detected = riso.detectObjects()
    riso.closeCamera()
    n_objs = len(detected)
    
    print ('{} object{} {} detected.\n'.format(n_objs, ""  if n_objs ==1 else 's', 'was' if n_objs ==1 else 'were'))

    if detected:
        
        coords_objs = np.array([[i[1] for i in detected], [i[2] for i in detected]]).T
        simul.plotObjects(coords_objs[:, 0], coords_objs[:, 1], n_objs*[0.0])
        for obj in detected:
            qObjs.put(obj)   
        
        while not qObjs.empty():
            img, x, y = qObjs.get()
            
            if i == max_iter:
                qClassObjs.put(('Undefined',x, y))
                
            else:
                result, prob = riso.classifyObject(img)
                if prob >= lim_prob:
                    qClassObjs.put((result, x, y))
                    
        n_class = qClassObjs.qsize()            
        print ('{}/{} objects were classified.\n'.format(n_class, n_objs))           
        
        while not qClassObjs.empty():
            if home:
                print ('RISO is moving to initial position.\n')
                riso.move([0.4, 0.0, 0.2])
                simul.plotRobot(riso) 
                home = False
                
            obj, x, y = qClassObjs.get()

            print ('{} at ({}, {}).\n'.format(obj if not i == max_iter else "Unclassified object", x, y))
            pos_efec = riso.move([x, y, 0.0])
            
            if pos_efec:                
                simul.plotRobot(riso)
                ind = np.where(np.all(np.isclose(coords_objs, np.array([x, y])), axis =1))
                coords_objs = np.delete(coords_objs, ind, 0)                
                simul.plotObjects(coords_objs[:, 0], coords_objs[:, 1], n_objs*[0.0])
                print ('Container at ({}, {}).\n'.format(containers[obj][0], containers[obj][1]))
                riso.move(containers[obj])
                simul.plotRobot(riso)
            else:
                print ('({}, {}) is unreachable'.format(x, y))
        
        if i == max_iter:
            break
        
    else:
        
        break
    
    
#riso.serial.close()
print ('The end!')     


