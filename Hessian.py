import math
from scipy import ndimage
from PIL import Image
from numpy import *
from matplotlib import pyplot as plt
from pylab import *
import cv2
import time
'''====================================================Procedure 'MarkCorner'======================================================'''
'''The following procedure marks corners in a given input image'''
def mcor (I, # input image
x, # x vertex of corner
y # y vertex of corner
):
        plt.figure()
	plt.imshow(I,cmap = cm.gray) # plot the image in grayscale
	plot(x,y,'r.') # mark the corners in red
	plt.axis([0,len(I[0,:]),len(I[:,0]),0])
        return show()


'''====================================================End of MarkCorner======================================================'''
def gmask (x,y,s): # the function for gaussian filter
    gmask = (1/(math.sqrt(2*(math.pi))*s))*exp(-((x**2) + (y**2))/2/s**2)
    return gmask
    
def gmask1 (x,y,s,z): # function implementing the first derivative of the gaussian filter
    if(z =='x'):
        gmask1 = gmask(x,y,s)*(-x/(s**2))
    elif(z=='y'):
        gmask1 = gmask(x,y,s)*(-y/(s**2))
    return gmask1
def gmask2 (x,y,s,z): # function implementing the second derivative of the gaussian filter
    if(z =='x'):
        gmask2 = gmask(x,y,s)*(((x**2)/(s**2))-1)/s**2
    elif(z=='y'):
        gmask2 = gmask(x,y,s)*(((x**2)/(s**2))-1)/s**2
    return gmask2
'''====================================================Procedure 'HESSIAN 1'======================================================'''
'''The following procedure is defined to dectect corners of an input image using hessian matrix'''
def hessian1(inp, # the input image name
s, # Standard Deviation value
t): # The threshold of eigen value to be considered as edge
    start = time.clock()
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
    
    Gx2 = []
    for i in range(-size,size+1):
        Gx2.append(gmask2(i,0,s,'x')) 
    
    Gy2 = []
    for i in range(-size,size+1):
        Gy2.append([gmask2(0,i,s,'y')]) 
    
    Ix = []
    for i in range(len(I[:,0])):
        Ix.extend([convolve(I[i,:],Gx)]) # I*G ----> x direction
    Ix = array(matrix(Ix))
    Iy = []
    for i in range(len(I[0,:])):
        Iy.extend([convolve(I[:,i],Gx)]) # I*G ----> y direction
    Iy = array(matrix(transpose(Iy))) 
    
    Ixx = []
    for i in range(len(Ix[:,0])):
        Ixx.extend([convolve(Ix[i,:],Gx2)]) # Ix * Gx ----> x direction
    Ixx = array(matrix(Ixx))
    
    Iyy = []  
    for i in range(len(Iy[0,:])):
        Iyy.extend([convolve(Ix[:,i],Gx2)]) # Iy * Gy ----> y direction
    Iyy = array(matrix(transpose(Iyy))) 
    
    Ixy = []
    for i in range(len(Iy[0,:])):
        Ixy.extend([convolve(Ix[:,i],Gx2)]) # Iy * Gy ----> y direction
    Ixy = array(matrix(transpose(Ixy))) 
    
    x = [] # this array stores the x vertex of corners
    y = [] # this array stores the y vertex of corners
    for i in range(len(I[:,0])):
        for j in range(len(I[0,:])):
            H1 = linalg.eigvals(([Ixx[i,j],Ixy[i,j]],[Ixy[i,j],Iyy[i,j]]))
            if((abs(H1[0])>t) & (abs(H1[1])>t)): # if corner
                y.append(i-2) # note the y index
		x.append(j-2) # note the x index
    				# using these indices, corners are marked
    mcor(I,x,y)
    return time.clock() - start
'''=====================================================End of Procedure HESSIAN 1=================================================='''
s = 1.5 # set the value for standard deviation
size = 2 # size = 2(input)+1 
time1 = hessian1('input1.png',s,3.95695) #3.95695
time2 = hessian1('input2.png',s,5) #5
time3 = hessian1('input3.png',s,4)
print 'The Accuracy is:\nInput Image 1: %.2fseconds\nInput Image 2: %.2fseconds\nInput Image 3: %.2fseconds)'%(time1,time2,time3)
'''=====================================================Conclusion start==================================================
In this algorithm, the corner repeatability increases as the overlap threshold is increased.
========================================================Conclusion end=================================================='''



