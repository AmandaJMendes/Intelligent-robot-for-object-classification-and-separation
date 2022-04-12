#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 13:41:22 2021

@author: amanda
"""

'''
This code contains a class for object detection and classification
'''

import json
import numpy as np
from tensorflow import lite




class ImageClassifier:
    
    '''
    This is a class for image classification
    '''
    
    def __init__ (self, img_shape, model_dir, classes_dir):
        
        '''
        img_shape: e.g.: (480, 480, 3) 
        model_dir: directory of trained model
        classes_dir: directory of file containing the classes' names
        classes: it is set when loadClasses() is called
        model: it is set when loadModel() is called            
        '''
        
        self.img_shape = img_shape 
        self.model_dir = model_dir 
        self.classes_dir = classes_dir 
        self.classes = None 
        self.model = None
        
        
    def loadModel(self):
        
        '''
        This method:
            Loads model from self.model_dir
            Saves the model and its input and output details to self.model
        '''
        
        model = lite.Interpreter(model_path= self.model_dir)
        model.allocate_tensors()
        input_details = model.get_input_details()
        output_details = model.get_output_details()       
        self.model =  (model, input_details, output_details)
    
    def loadClasses(self):
        
        '''
        This method:
            Loads file with classes' names from self.classes_dir
            Saves it to self.classes
        '''
        
        with open(self.classes_dir) as names:
            self.classes = json.load(names)
        
    def classifyObject(self, obj_array):
        
        '''
        This method:
            Uses self.model to predict class of obj_array
            Returns:
                obj_class: predicted class of obj_array
                obj_probab: certainty of the prediction (0 - 100)
        '''
        
        self.model[0].set_tensor(self.model[1][0]['index'], obj_array)    
        self.model[0].invoke()
        classification = self.model[0].get_tensor(self.model[2][0]['index'])
        obj_class = str(self.classes[np.argmax(classification)])
        obj_probability = round(float(np.max(classification))*100,5)
               
        return obj_class, obj_probability
        
if __name__ == '__main__':
    
    from queue import Queue
    from image import ObjectDetector
    
    qClassObjs = Queue()
    model_dir = 'modeloNovo.tflite'
    classes_dir = 'modelo.txt'
    img_shape = (200,200,3)

    classifier = ImageClassifier(img_shape, model_dir , classes_dir)
    classifier.loadModel()
    classifier.loadClasses()

    qObjs = Queue()
    #img_shape = (200,200,3)    
    detector = ObjectDetector(img_shape, 0.3, 0.3)
    
    
    detec = input('Realizar detecção e classificação de objetos?')
    
    while detec:
        detector.openCamera()
        detected = detector.detectObjects()
        detector.closeCamera()
        for obj in detected:
            qObjs.put(obj) 
        
        n_objs = qObjs.qsize()
        
        while not qObjs.empty():
            
            obj, x, y = qObjs.get()
            obj_class, obj_prob = classifier.classifyObject(obj)
            
            if obj_prob > 99.99:
                print ('\n--- {} detectad{} em ({}, {})\n'.format(obj_class,'a' if obj_class == 'Porca' else 'o', x, y))
                qClassObjs.put((obj_class, x, y))
                
            else:
                print ('Indefinido')
        
        print ('Total de {} objetos.\n\n'.format(n_objs))
        
        detec = input('Realizar detecção e classificação de objetos?')
        
    