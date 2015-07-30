# -*- coding: utf-8 -*-
"""
Created on Sun May 24 22:02:49 2015

@author: Ron
"""
from numpy import sin, cos, pi, asarray, array, shape, zeros
from scipy.stats import norm
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage.filters import median_filter

class vec:
    def __init__(self,x,y,u,v,chc,dt,lUnits='m',tUnits='s'):
        """ basic class that will hold the velocity field
            x,y are coordinates in lUnits
            u,v are velocity components in lUnits/tUnits
            CHC is some marker of bad vectors
            theta is not so clear but it's a global orientation angle, in degrees
            properties:
            lUnits, default is 'm'
            tUnits, default is 's'
            velUnits, derived from  lUnits, tUnits
        """
        self.x = x
        self.y = y
        self.u = u
        self.v = v
        self.chc = chc
        self.dt = dt
        self.lUnits = lUnits
        self.tUnits = tUnits
        self.velUnits = lUnits + '/' + tUnits
        self.theta = 0.0 # what is theta ? 
    
    def set_dt(self,dt):
        self.dt = dt
    
    def get_dt(self):
        return self.dt
    
    def set_Lunits(self,Lunits = 'm'):
        self.lUnits = lUnits # default is meter
    
    def set_tUnits(self,tUnits = 's'):
        self.tUnits = tUnits # default is sec
            
    def rotate(self,theta=0.0):
        """ 
        use this method in order to rotate the data 
        by theta degrees in the clockwise direction
        """
        
        theta = theta/360.0*2*pi
        
        xi = self.x*cos(theta) + self.y*sin(theta)
        eta = self.y*cos(theta) - self.x*sin(theta)
        Uxi = self.u*cos(theta) + self.v*sin(theta)
        Ueta = self.v*cos(theta) - self.u*sin(theta)
        self.x, self.y = xi, eta
        self.u, self.v  = Uxi, Ueta
        self.theta = self.theta + theta # this is not clear what theta defines 
        
    def scale(self,resolution):
        """
        use this method to fux the resolution of the 
        vector from [px/frame] to [m/sec] or any similar
        - resolution should be in [length/px]
        - time is generated from the original file and
          it is in seconds - BUG: MICROSECONDS?
        """
        self.x = self.x*resolution
        self.y = self.y*resolution
        self.u = self.u*resolution/(self.dt*1e-6) #BUG: MICROSECONDS?
        self.v = self.v*resolution/(self.dt*1e-6)
        
    def move(self,dx,dy):
        """
        use this method to move the origin of the frame
        by dx and dy
        """
        self.x = self.x + dx
        self.y = self.y + dy

        
    def crop(self,xmin,xmax,ymin,ymax):
        """
        this method is used to crop a rectangular section 
        of the vector field difined as the region between 
        (xmin,ymin) and (xmax,ymax) 
        """
        temp = []
        indexes = []
        for i in range(len(self.x[:,0])):
            temp.append([])
            for j in range(len(self.x[0,:])):
                if self.x[i,j]<xmax and self.x[i,j]>xmin:
                    if self.y[i,j]<ymax and self.y[i,j]>ymin:
                        temp[-1].append((i,j))
        for i in temp:
            if len(i)>0:
                indexes.append(i)
        if len(indexes)==0:
            print 'not valid crop values'
            return
        indexes = array(indexes)
        x, y = zeros(shape(indexes[:,:,0])), zeros(shape(indexes[:,:,0]))
        u, v = zeros(shape(indexes[:,:,0])), zeros(shape(indexes[:,:,0]))
        chc = zeros(shape(indexes[:,:,0]))
        for i in range(len(indexes)):
            for j in range(len(indexes[i])):
                x[i,j] = self.x[indexes[i,j][0],indexes[i,j][1]]
                y[i,j] = self.y[indexes[i,j][0],indexes[i,j][1]]
                u[i,j] = self.u[indexes[i,j][0],indexes[i,j][1]]
                v[i,j] = self.v[indexes[i,j][0],indexes[i,j][1]]
                chc[i,j] = self.chc[indexes[i,j][0],indexes[i,j][1]]
        self.x = x
        self.y = y
        self.u = u
        self.v = v
        self.chc = chc
        
    def getVelStat(self):
        """
        assuming normaly distributed values of U and V in the
        data, this method calculates its mean and standard
        deviation values and assigns them to new atribtes
        of the instance vec.
        this methid does not take into account values of 
        the velocity that insight had spotted as irregular
        values (aka CHC=-1)
        """
        # we need to use numpy way:
        
        u = self.u.flatten()
        v = self.v.flatten()
        self.Umean, self.Ustd = norm.fit(u)
        self.Vmean, self.Vstd = norm.fit(v)
        
    def filterVelocity(self,filtr = 'med',size=(4,4)):
        """
        this method passes the velocity vectors U and V
        through a either a 4 x 4 median filter or a gaussian
        filter with sigma = 1
        Inputs: 
            filtr = 'med' (default), 'gauss', string
            size  = (4,4) default, tuple
        """
        if filtr == 'med':
            self.u = median_filter(self.u,size=size)
            self.v = median_filter(self.v,size=size)
        elif filtr == 'gauss':
            self.u = gaussian_filter(self.u,1)
            self.v = gaussian_filter(self.v,1)
        else: print "Bad choise of filter! - try again"