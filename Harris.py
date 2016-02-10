import math
from scipy import ndimage
from PIL import Image
from numpy import *
from matplotlib import pyplot as plt
from pylab import *
import time
def gmask (x,y,s): # the function for gaussian filter
    gmask = (1/(math.sqrt(2*(math.pi))*s))*exp(-((x**2) + (y**2))/2/s**2)
    return gmask
    
def gmask1 (x,y,s,z): # function implementing the first derivative of the gaussian filter
    if(z =='x'):
        gmask1 = gmask(x,y,s)*(-x/(s**2))
    elif(z=='y'):
        gmask1 = gmask(x,y,s)*(-y/(s**2))
    return gmask1
'''====================================================Function 'Harris 1'======================================================'''
'''The following function is defined to dectect corners of an input image using harris matrix, the function also returns the run time'''
def Harris(file # name of input image file
,size # size of the kernal size = 2(input)+1
,a # aplha, the cornerness parameter.
,t, # threshold 
s # sigma value....
):
    start = time.clock()
    inp = file # input image
    I = array(Image.open(inp).convert('L')) # read the input image
    G = []
    for i in range(-2,2+1):
        G.append(gmask(i,0,s)) # equating y to 0 since we need a 1D matrix
    Gx = []
    for i in range(-size,size+1):
        Gx.append(gmask1(i,0,s,'x')) 
   	
    Gy = []
    for i in range(-size,size+1):
        Gy.append([gmask1(0,i,s,'y')]) 
    
    I1 = []
    for i in range(len(I[:,0])):
   	I1.extend([convolve(I[i,:],G)]) # I*G ----> x direction
    I1 = array(matrix(I1))
    I11 = I1*I1
    
    Ix = []
    for i in range(len(I[:,0])):
   	Ix.extend([convolve(I1[i,:],Gx)]) # I*G ----> x direction
    Ix = array(matrix(Ix))
    
    I2 = []
    for i in range(len(I[0,:])):
   	I2.extend([convolve(I[:,i],G)]) # I*G ----> y direction
    I2 = array(matrix(transpose(I2))) 
    I22 = I2*I2
    
    Iy = []
    for i in range(len(I[0,:])):
   	Iy.extend([convolve(I2[:,i],Gx)]) # I*G ----> y direction
    Iy = array(matrix(transpose(Iy))) 
    
    I12 = []
    for i in range(len(I1[:,0])):    
        temp = []
        for j in range(len(I2[0,:])):    
   	    temp.append(I1[i,j]*I2[i,j])
   	if (j == len(I2[0,:])-1):
                I12.extend(array(matrix(temp)))
    I12 = array(matrix(I12))
    
    
    Ixy = []
    for i in range(len(I12[:,0])):
   	Ixy.extend([convolve(I12[i,:],Gx)]) # I*G ----> x direction
    Ixy = array(matrix(Ixy))
    
    
    
    x = [] # this array stores the x vertex of corners
    y = [] # this array stores the y vertex of corners
    for i in range(len(I[:,0])):
        for j in range(len(I[0,:])):
            H1 = ([Ix[i,j]**2,Ix[i,j]*Iy[i,j]],[Ix[i,j]*Iy[i,j],Iy[i,j]**2]) # Harris Matrix
            if(abs(linalg.det(H1)-(a*(trace(H1)))) > t): # if a corner # if a corner                
                y.append(i-5)
                x.append(j-5)
    
    plt.figure()
    plt.imshow(I,cmap = cm.gray)
    plot(x,y,'r.')
    plt.axis([5,len(I[0,:]),len(I[:,0]),5])
    show()
    return time.clock() - start

#size = 2
    #a = .055 #.05
    #t = 30#21.79 # 43.999
    #s = 1.5 #1.3 #set the value for standard deviation
time1 = Harris('input1.png',2,.03,16.5,1.5)
time2 = Harris('input2.png',2,.004,4.55,1.5)
time3 = Harris('input3.png',2,.004,1,1.5)
print 'The Accuracy is:\nInput Image 1: %.2fseconds\nInput Image 2: %.2fseconds\nInput Image 3: %.2fseconds)'%(time1,time2,time3)
'''=====================================================Conclusion start==================================================
Accuray of this algoritm is better than the next one.
========================================================Conclusion end=================================================='''

