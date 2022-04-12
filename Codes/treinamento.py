#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 10:38:20 2020

@author: amanda
"""

import numpy as np
import os 
from tensorflow import keras, lite
import cv2
from sklearn import preprocessing
import json
from sklearn.model_selection import train_test_split


class Treinamento:
    
    def __init__(self, input_shape):
        
        self.input_shape = input_shape
        self.images = []
        self.classes = []
        
    def carregaImagens(self, directory, label):
        
        for file in os.listdir(directory): 
            img_ar=cv2.imread(directory+file)
            self.images.append(img_ar)
            self.classes.append(label)

    def preparaImagens(self):
        
        self.le = preprocessing.LabelEncoder() #LaberBinarizer talvez dispense o uso do to_categorical, mas só funcina com mais de 2 classes
        labels = self.le.fit_transform(self.classes)
        return  train_test_split(np.asarray(self.images).astype('float32') / 255,
                                                            keras.utils.to_categorical(labels) , test_size=0.1, random_state=42)
    
    def treina (self, X_train, X_test, y_train, y_test):
        
        model = keras.models.Sequential()

        model.add(keras.layers.Conv2D(32, (2,2), input_shape=self.input_shape,activation='relu'))

        model.add(keras.layers.MaxPooling2D((2,2)))
        model.add(keras.layers.Conv2D(32, (2, 2), activation='relu'))
        
        model.add(keras.layers.MaxPooling2D((2,2)))
        model.add(keras.layers.Conv2D(64, (2, 2), activation='relu'))
        
        model.add(keras.layers.MaxPooling2D((2,2)))
        model.add(keras.layers.Conv2D(64, (2, 2), activation='relu'))
        
        model.add(keras.layers.MaxPooling2D((2, 2)))
        model.add(keras.layers.Conv2D(128, (2, 2), activation='relu'))
        
        model.add(keras.layers.Flatten())
        model.add(keras.layers.Dense(64, activation='relu'))
        model.add(keras.layers.Dropout(0.2))
        model.add(keras.layers.Dense(32, activation='relu'))
        model.add(keras.layers.Dropout(0.2))
        model.add(keras.layers.Dense(2, activation= 'softmax'))
        
        model.compile(loss='binary_crossentropy',
                      optimizer='Adam',
                      metrics=['accuracy'])
        
        history  = model.fit(X_train,y_train,epochs=2, batch_size=1,validation_data=(X_test, y_test))
        return (model, history.history['val_accuracy'][-1])
    
    def salva_tflite(self, modelo, diretorio):
        
        converter = lite.TFLiteConverter.from_keras_model(modelo)
        tflite_model = converter.convert()
        with open(diretorio+'modeloNovo.tflite', 'wb') as f:
            f.write(tflite_model)
        with open(diretorio + 'modeloNovo.txt', "w+") as output:
            json.dump((list(self.le.classes_)), output)
 


if __name__ == '__main__':
    
    t = Treinamento((200, 200, 3))
    t.carregaImagens('/home/amanda/Área de Trabalho/RISO/CódigosImportantes/Treinamento/Porcas/', "Porca")
    t.carregaImagens('/home/amanda/Área de Trabalho/RISO/CódigosImportantes/Treinamento/Parafusos/', "Parafuso")
    X_train, X_test, y_train, y_test = t.preparaImagens()
    modelo = t.treina(X_train, X_test, y_train, y_test)
    #t.salva_tflite(modelo[0],'/home/amanda/Área de Trabalho/RISO/')
