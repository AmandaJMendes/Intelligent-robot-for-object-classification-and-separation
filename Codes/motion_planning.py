
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 12:34:16 2021

@author: amanda
"""

'''
This code contains classes for motion planning
'''

import numpy as np

class Path:
    
    '''
    This is a path
    '''
    
    def __init__ (self, ti, tf, initial, final):
        
        '''
        t: array of instants (initial and final)
        coords: array of joint coordinates (inital and final)
        '''
        
        self.t = np.array([[ti], [tf]])
        self.coords = np.array([[i for i in initial], [i for i in final]])
        
        
class Trajectory:
    
    '''
    This is a trajectory generator
    This class generates a trajectory from a Path object
    '''
    
    def __init__ (self, path, step):
        
        '''
        path: Path object
        step: generator's step 
        '''
        
        self.path = path
        self.step = step
        self.t = path.t[0][0]
        self.counter = 0
        self.interval = path.t[1][0] - path.t[0][0]
        self.n_points = int(self.interval/step)
        self.n_joints = path.coords.shape[1]
    
    def generateCoord(self):
        
        '''
        This method is implemented in Child class
        '''
        raise NotImplementedError
        
    def __iter__ (self):
        
        '''
        This method defines the class as a generator
        '''
        
        return self
    
    def __next__ (self):
        
        '''
        This method:
            Allows generator class to be used in a loop (each iteration increases self.t by step). 
            Returns the trajectory point calculated for current instant (self.t)
        '''
        
        if self.counter <= self.n_points:
            coord =  self.generateCoord()
            self.t += self.step
            self.counter += 1
        else:
            self.t = 0.0
            self.counter = 0.0
            raise StopIteration
        return coord   
    
    def generateAll(self):
        
        '''
        This method returns a list of all the points of the trajectory
        '''
        
        allCoords = []
        for i in self:
            allCoords.append(i)
        return allCoords

class PolyTrajectory(Trajectory):
    
    '''
    This is a Polynomial Trajectory generator .
    This class is a Trajectory's child.     
    '''
    
    def __init__ (self, path, step):
        
        '''
        This constructor initializes a Trajectory object (Parent)
        polynomials: list of the polynomials that describe movement of each joint.
        Each list in self.polynomials contains 3 polynomials (coordinate,
        velocity, acceleration)
        '''
        
        Trajectory.__init__(self, path, step)
        self.polynomials = []
        
    def createPolynomials(self):
        
        '''
        This method calculates polynomials that describe the movement of each joint (coordinate,
        velocity, acceleration) based on inital and final values
        Polynomials are appended to self.polynomials
        '''
        
        time_coeffs = np.eye(6,6)
        time_coeffs[2, 2]=time_coeffs[5, 2]=2
        time_coeffs[3, 0]=time_coeffs[4, 1] = 1
        time_coeffs[3, 1]=self.path.t[1][0]
        time_coeffs[3, 2]=self.path.t[1][0]**2
        time_coeffs[3, 3]=self.path.t[1][0]**3
        time_coeffs[3, 4]=self.path.t[1][0]**4
        time_coeffs[3, 5]=self.path.t[1][0]**5
        time_coeffs[4, 2]=2*time_coeffs[3, 1]
        time_coeffs[4, 3]=3*time_coeffs[3, 2]
        time_coeffs[4, 4]=4*time_coeffs[3, 3]
        time_coeffs[4, 5]=5*time_coeffs[3, 4]       
        time_coeffs[5, 3]=6*time_coeffs[3, 1]
        time_coeffs[5, 4]=12*time_coeffs[3, 2]
        time_coeffs[5, 5]=20*time_coeffs[3, 3]
        
        coord = np.zeros((6, self.n_joints))
        coord[0] = self.path.coords[0]
        coord[3] = self.path.coords[1]
        poly_coeffs = np.dot(np.linalg.inv(time_coeffs), coord)[::-1]
        
        for i in range(self.n_joints):
            coeffs = poly_coeffs[:,i]
            polynomials_i = [np.poly1d(coeffs, variable='t'),
                              np.poly1d([5*coeffs[0], 4*coeffs[1], 3*coeffs[2], 2*coeffs[3], coeffs[4]], variable='t'),
                              np.poly1d([20*coeffs[0], 12*coeffs[1], 6*coeffs[2], 2*coeffs[3]], variable='t')]
            self.polynomials.append(polynomials_i)

    def generateCoord(self):
        
        '''
        This method:
            Generates the next point in the trajectory using the previously calculated polynomials
            Returns:
                coord: list containing instant and array with coordinate, velocity and acceleration of each joint 
        '''
        
        coord = [self.t,np.zeros((3,self.n_joints))]
        for i in range(self.n_joints):
            for j in range(3):
                coord[1][j][i] = self.polynomials[i][j](self.t)
        return coord
    


   
if __name__ == '__main__':
     
    import matplotlib.pyplot as plt

    def plotMovement(points, n_joints, graphic = None):    
        
        instants = [i[0] for i in points]            
        values = np.array([i[1] for i in points])
        
        if not graphic:     
            fig, axs = plt.subplots(n_joints, sharex = True, figsize=(10,20))
            for i in range(n_joints):
                axs[i].plot(instants, values[:, 0, i], label = 'Ângulo')
                axs[i].plot(instants, values[:, 1, i], label = 'Velocidade')
                axs[i].plot(instants, values[:, 2, i], label = 'Aceleração')
            lines, labels = fig.axes[0].get_legend_handles_labels()
            fig.legend(lines, labels, loc = 'upper center', ncol = 3)
        
        elif graphic == 'p':            
            plt.figure(figsize=(8,4))
            plt.plot(instants, [i[0, 0] for i in values], color = (0.6, 0.0, 0.2))
            plt.title('Posição x Tempo')
            plt.xlabel('Tempo')
            plt.ylabel('Posição')
            
        elif graphic == 'v':
            plt.figure(figsize=(8,4))
            plt.plot(instants, [i[1, 0] for i in values], color = (0.6, 0.0, 0.2))
            plt.title('Velocidade x Tempo')
            plt.xlabel('Tempo')
            plt.ylabel('Velocidade')
            
        elif graphic == 'a':
            plt.figure(figsize=(8,4))
            plt.plot(instants, [i[2, 0] for i in values], color = (0.6, 0.0, 0.2))
            plt.title('Aceleração x Tempo')
            plt.xlabel('Tempo')
            plt.ylabel('Aceleração')
            
        plt.show(block = False) 
        
    p = Path(0, 10, [0,0,0,0], [10,20,30,40])
    traj = PolyTrajectory(p,0.2)
    traj.createPolynomials()
    points = traj.generateAll()
    plotMovement(points, traj.n_joints)
    plotMovement(points, traj.n_joints, graphic = 'p')
    plotMovement(points, traj.n_joints, graphic = 'v')
    plotMovement(points, traj.n_joints, graphic = 'a')

    for i in traj:
        print ("Ângulo, velocidade e aceleração das {} juntas em {} segundos: \n{}\n\n\n".format(traj.n_joints,i[0], i[1]))

