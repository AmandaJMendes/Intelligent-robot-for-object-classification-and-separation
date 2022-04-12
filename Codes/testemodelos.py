#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 18:38:11 2021

@author: amanda
"""


from treinamento import Treinamento
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

porcas = '/home/amanda/Área de Trabalho/RISO/CódigosImportantes/Treinamento/Porcas/'
parafusos = '/home/amanda/Área de Trabalho/RISO/CódigosImportantes/Treinamento/Parafusos/'

t = Treinamento((200,200,3))
t.carregaImagens(porcas, 'Porca')
t.carregaImagens(parafusos, 'Parafuso')
X_train, X_test, y_train, y_test = t.preparaImagens()
cnn_acc = round(t.treina(X_train, X_test, y_train, y_test)[1], 4)


rf = RandomForestClassifier(n_estimators=2)
rf.fit(X_train.reshape(X_train.shape[0], X_train.shape[1] * X_train.shape[2] * X_train.shape[3]), y_train)
y_pred = rf.predict(X_test.reshape(X_test.shape[0], X_test.shape[1] * X_test.shape[2] * X_test.shape[3])) 
rf_acc = round(accuracy_score(y_test, y_pred), 4)

mlp = MLPClassifier(solver='lbfgs',random_state=1, hidden_layer_sizes = (5,))
mlp.fit(X_train.reshape(X_train.shape[0], X_train.shape[1] * X_train.shape[2] * X_train.shape[3]), y_train)
y_pred = mlp.predict(X_test.reshape(X_test.shape[0], X_test.shape[1] * X_test.shape[2] * X_test.shape[3])) 
mlp_acc = round(accuracy_score(y_test, y_pred),4)

plt.bar(['Random Forest', 'Multilayer Perceptron', 'Convolutional Neural Network'], [rf_acc, mlp_acc, cnn_acc], width = 0.5, color = (0.6, 0.0, 0.2) )
plt.title('Comparação de modelos de aprendizado de máquina para classificação de imagens de porcas e parafusos')
plt.xlabel('Algoritmos', fontsize = 'large', fontweight = 'bold')
plt.ylabel('Acurácia', fontsize = 'large', fontweight = 'bold')

plt.show(block  = False)
