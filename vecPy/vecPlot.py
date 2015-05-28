# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:04:24 2015

@author: Ron

This module contains function that help generating
velocity attributes of the .vec files that were open.
use this code over vec objects.
"""

import numpy as np
from numpy import *
from matplotlib.pylab import *
import matplotlib.pylab as mpl

def genQuiver(vec):
    """
    this function will generate a quiver plot from a vec 
    object    
    """
    mpl.contourf(vec.x,vec.y,sqrt(vec.u**2+vec.v**2),alpha=0.3)
    cbar = mpl.colorbar()
    cbar.set_label(r'Velocity [m $\cdot$ s$^{-1}$]')
    mpl.quiver(vec.x,vec.y,vec.u,vec.v,units='width',scale=amax(sqrt(vec.u**2+vec.v**2))*25.0,headwidth=2 )
    mpl.xlabel('x [' + vec.lUnits + ']')
    mpl.ylabel('y [' + vec.lUnits + ']')
    
    
def genVelHist(vec):
    """
    this function will plot a normalized histogram of
    the velocity data. the velocity in the histpgram 
    contains all the data set such that CHC == 1
    """
    u1,v1 = vec.U.flatten() , vec.V.flatten()
    ax1 = plt.subplot2grid((2,1),(0,0))
    ax1.hist(u1,bins=np.sqrt(len(u1))*0.5,normed=1)
    ax1.set_xlabel('u [mm/sec]')
    ax2 = plt.subplot2grid((2,1),(1,0))
    ax2.hist(v1,bins=np.sqrt(len(v1)*0.5),normed=1)
    ax2.set_xlabel('v [mm/sec]')
    plt.tight_layout()
    return
    
def genVorticityMap(vec):
    dUy = gradient(vec.U)[0]*cos(vec.theta)-gradient(vec.U)[1]*sin(vec.theta)
    dVx = gradient(vec.V)[1]*cos(vec.theta)+gradient(vec.V)[0]*sin(vec.theta)
    dx = gradient(vec.X)[1]*cos(vec.theta)+gradient(vec.X)[0]*sin(vec.theta)
    dy = gradient(vec.Y)[0]*cos(vec.theta)-gradient(vec.Y)[1]*sin(vec.theta)
    print amax(dUy),amax(dVx),amax(dx),amax(dy)
    vorticity = dVx/dy-dUy/dx
    plt.contourf(vec.X,vec.Y,vorticity)
    plt.xlabel('x ['+vec.length+']')
    plt.ylabel('y ['+vec.length+']')
    cbar = plt.colorbar()
    cbar.set_label(r'Vorticity [s$^{-1}$]')
    return