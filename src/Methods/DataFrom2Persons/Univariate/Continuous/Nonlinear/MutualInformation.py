### This file is a part of the Syncpy library.
### Copyright 2015, ISIR / Universite Pierre et Marie Curie (UPMC)
### Main contributor(s): Giovanna Varni, Marie Avril,
### syncpy@isir.upmc.fr
### 
### This software is a computer program whose for investigating
### synchrony in a fast and exhaustive way. 
### 
### This software is governed by the CeCILL-B license under French law
### and abiding by the rules of distribution of free software.  You
### can use, modify and/ or redistribute the software under the terms
### of the CeCILL-B license as circulated by CEA, CNRS and INRIA at the
### following URL "http://www.cecill.info".

### As a counterpart to the access to the source code and rights to
### copy, modify and redistribute granted by the license, users are
### provided only with a limited warranty and the software's author,
### the holder of the economic rights, and the successive licensors
### have only limited liability.
### 
### In this respect, the user's attention is drawn to the risks
### associated with loading, using, modifying and/or developing or
### reproducing the software by the user in light of its specific
### status of free software, that may mean that it is complicated to
### manipulate, and that also therefore means that it is reserved for
### developers and experienced professionals having in-depth computer
### knowledge. Users are therefore encouraged to load and test the
### software's suitability as regards their requirements in conditions
### enabling the security of their systems and/or data to be ensured
### and, more generally, to use and operate it in the same conditions
### as regards security.
### 
### The fact that you are presently reading this means that you have
### had knowledge of the CeCILL-B license and that you accept its terms.

"""
.. moduleauthor:: Giovanna Varni
"""
import sys
sys.path.insert(0, '../src/')

import numpy as np
import pandas as pd
import random

from scipy.spatial import cKDTree
from scipy.special import psi

from Method import Method, MethodArgList

class MutualInformation(Method):
    """
    It computes Mutual Information (MI) estimators starting from entropy estimates from k-nearest-neighbours distances.
    
    **Reference :**
    
    * A.Kraskov, H.Stogbauer, and P.Grassberger. Estimating mutual information. Physical Review E, 69(6):066138, 2004
    
    :param n_neighbours:
        number of nearest neighbours  
    :type n_neighbours: int
    
    :param my_type:
        Type of the estimators will be used to compute MI. Two options (1 and 2) are available:
            1. the number of the points nx and ny is computed by taking into account only the points whose distance is stricly
            less than the distance of the k-nearest neighbours; 
            2. the number of the points nx and ny is computed by taking into account only the points whose distance is equal to
            or less than the distance of the k-nearest neighbours; 
       Default: 1 
    :type my_type: int
    
    :param var_resc:
        Boolean value indicating if the input signals should be rescaled at unitary variance. Default: False
    :type var_resc: bool
    
    :param noise:
        Boolean value indicating if a very low amplitude random noise should be added to the signals.
        It is done to avoid that there are many signals points having identical coordinates. Default: True
    :type noise: bool
        
    """
    argsList = MethodArgList()
    argsList.append('n_neighbours', 10, int, 'number of the nearest neighbours to be used')
    argsList.append('my_type', 1, int, 'the type of estimators [1 or 2]')
    argsList.append('var_resc', False, bool, 'signals should be rescaled at unitary variance')
    argsList.append('noise', True, bool, 'adding random noise to the time series')
    
    ''' Constuctor '''
    def __init__(self, n_neighbours, my_type=1, var_resc=True, noise=True, **kwargs):
        super(MutualInformation, self).__init__(plot=False,**kwargs)
        ' Raise error if parameters are not in the correct type '
        try :
            if not(isinstance(n_neighbours, int)) : raise TypeError("Requires n_neighbours to be an integer")
            if not(isinstance(my_type, int))      : raise TypeError("Requires my_type to be an integer")
            if not(isinstance(var_resc, bool))    : raise TypeError("Requires var_resc to be a boolean")
            if not(isinstance(noise, bool))    : raise TypeError("Requires noise to be a boolean")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return
        
        ' Raise error if parameters do not respect input rules '
        try :
            if n_neighbours<=0: raise ValueError("Requires n_neighbours to be a positive integer greater than 0")
            if my_type != 1  and my_type != 2 : raise ValueError("Requires my_type to be to be 1 or 2" )
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
        
        self.n_neighbours=n_neighbours
        self.type=my_type
        self.var_resc=var_resc
        self.noise=noise
        

    def compute(self,signals):
        """
        It computes Mutual Information.
         
        :param x:
            first input signal
        :type x: pd.DataFrame
        
        :param y:
            second input signal
        :type y: pd.DataFrame
      
        :returns: dict
            -- Mutual Information
        """
        x = signals[0]
        y = signals[1]
        
        ' Raise error if parameters are not in the correct type '
        try :
            if not(isinstance(x, pd.DataFrame)) : raise TypeError("Requires x to be a pd.DataFrame")
            if not(isinstance(y, pd.DataFrame)) : raise TypeError("Requires y to be a pd.DataFrame")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return
        
        x.astype(np.float64)
        y.astype(np.float64)
        
        #pd.set_option('display.precision', 13) #to print pandas dataframe with 13 digits (12 decimals)
        #np.set_printoptions(precision=13) #to print np array with 13 digits
        
        #random noise generation 
        if self.noise==True:        
            rnoise_x=pd.DataFrame(1.0*np.random.rand(x.shape[0],1)/1e10,x.index)
            rnoise_x.astype(np.float64)
        
            rnoise_y=pd.DataFrame(1.0*np.random.rand(x.shape[0],1)/1e10,y.index)
            rnoise_y.astype(np.float64)

            x.iloc[:,0] += rnoise_x.iloc[:,0]
            y.iloc[:,0] += rnoise_y.iloc[:,0] 

        #rescaling of the time series
        if self.var_resc==True:
            xstd=((x-x.mean(axis=0))/x.std(axis=0))-x.min()
            ystd=((y-y.mean(axis=0))/y.std(axis=0))-y.min()
            
            x=xstd-xstd.min()
            y=ystd-ystd.min()
 
        #building z time series vector
        z=pd.concat([x,y],axis=1)
        
        z.astype(np.float64)
        
        d=np.array([])
        idx=np.array([])
        
        d.astype(np.float64,order='C')
        
        dx=np.array([])
        dx.astype(np.float64,order='C')
        
        dy=np.array([])
        dy.astype(np.float64,order='C')
        
        dz=np.array([])
        dz.astype(np.float64,order='C')

        
        #looking for the k nearest neighbours
        tree=cKDTree(z)
         
        for i in range(0,z.shape[0]):
            di,idxi=tree.query(z.iloc[i].values,k=self.n_neighbours+1,p=np.inf) 

             
            dx_abs=(np.abs(x.iloc[idxi].values-z.iloc[i,0]))
            dx_abs=np.delete(dx_abs,np.where(dx_abs==0))
                        
            dx_i=np.max(dx_abs)

            dx=np.append(dx,dx_i)


            dy_abs=(np.abs(y.iloc[idxi].values-z.iloc[i,1]))
            dy_abs=np.delete(dy_abs,np.where(dy_abs==0))
                        
            dy_i=np.max(dy_abs)
            dy=np.append(dy,dy_i)
            
            
            dz_i=max(dx_i,dy_i)
            dz=np.append(dz,dz_i)

            
            
        nx=np.array([])
        ny=np.array([])
                
        
        #Estimator 1             
        if self.type==1:
                        
            for i in range(0,x.shape[0]):
                
                nx_i=np.count_nonzero((np.array((np.abs(x.subtract(x.iloc[i])))).astype(np.float64,order='C')) < dz[i] )

                if nx_i > 0:
                    nx_i=nx_i-1
                
                nx=np.append(nx,nx_i)
                
                ny_i=np.count_nonzero((np.array((np.abs(y.subtract(y.iloc[i])))).astype(np.float64,order='C')) < dz[i])
            
                   
                if ny_i > 0:
                    ny_i=ny_i-1
            
                ny=np.append(ny,ny_i)
                            
            psi_xy=(psi(nx+1)+psi(ny+1))
                
            MI = psi(self.n_neighbours)+psi(z.shape[0])-np.mean(psi_xy)
            
        # Estimator 2   
        elif self.type==2:
            
            for i in range(0,x.shape[0]):
                
                nx_i=np.count_nonzero((np.array((np.abs(x.subtract(x.iloc[i])))).astype(np.float64,order='C'))<= dx[i] )
                

                if nx_i > 0:
                    nx_i=nx_i-1
                
                nx=np.append(nx,nx_i)
            
                ny_i=np.count_nonzero((np.array((np.abs(y.subtract(y.iloc[i])))).astype(np.float64,order='C'))<= dy[i])
            
                   
                if ny_i > 0:
                    ny_i=ny_i-1
            
                ny=np.append(ny,ny_i)
                        
            psi_xy=(psi(nx)+psi(ny))
            
            MI = psi(self.n_neighbours)+psi(z.shape[0])-(1.0/self.n_neighbours)-np.mean(psi_xy)
        
        results = dict()
        results['MI'] = MI
        
        return results

    @staticmethod
    def getArguments():
        return MutualInformation.argsList.getMethodArgs()

    @staticmethod
    def getArgumentsAsDictionary():
        return MutualInformation.argsList.getArgumentsAsDictionary()

    