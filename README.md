# Intelligent-robot-for-object-classification-and-separation

This was a final project for the Industrial Automation technical course in the Federal Institute of Rio Grande do Sul (IFRS) developed by me and Kauã Ortiz Silveira. @KauaOrtiz

### RISO: Robô Inteligente Separador e Organizador (Intelligent robot for object classification and separation)
#### Amanda Jorge Mendes, Kauã Ortiz Silveira
##### Advisor: Carlos Rodrigues Rocha
##### Co-advisor : Betânia Vargas Oliveira

### Abstract:
This project proposes the construction of a robotic system aiming object recognition, classification and separation using computer vision. The system’s components consist of a delimted surface, where the objects are going to be placed, a camera to capture the images, which are going to be processed by the computer vision and machine learning algorithms, stepper motors, to move the robot’s joints, and a simulation of the manipulator’s kinematic chain, since it wasn’t possible to bluid its mechanical structure. This project explores the intersection of robotics aspects such as kinematic operations, trajectory generation and motor controlling, and artificial intelligence techniques, such as the use of machine learning in computer vision. The implemented system can be used for didatic purposes as well as for research on methods for object recognition, classification and separatio

## Description of Codes folder

* testemodelos.py: test of different techniques for image classification
* treinamento.py: training a convolutional neural network with Keras/Tensorflow
* TCCMotores.py: ESP32 motor controlling with MicroPython
* kinematics.py: kinematic operations
* motion_planning.py: motion planning/trajectory generation
* image.py: object detector
* classification.py: image classification
* riso.py: RISO's functions (using kinematics.py, motion_planning.py, image.py and classification.py)
* plotRobot.py: simulation of robot's movement
* modelo.txt: classification info
* modeloNovo.tflite: model used for classification
