### This file was generated for use with the Syncpy library.
### Copyright 2016, ISIR / Universite Pierre et Marie Curie (UPMC)
### syncpy@isir.upmc.fr
###
### Main contributor(s): Jean Zagdoun
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
.. moduleauthor:: Jean Zagdoun
"""
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=RuntimeWarning)
from Method import Method, MethodArgList
from utils import Standardize
import numpy as np
from numpy.linalg import eig
from numpy.linalg import inv
from numpy.linalg import svd
from numpy import diag
from math import sqrt
import pandas as pd

class CCA(Method):
   """
   extract the highest correlations possible between projections of the features of the two datasets.
   datasets must contain the same number of row (individual or sample)
   But can contain different number of feature (i.e different number of rows)
   
   returns the weight of projections
   and correlations that comes with those weights
   """
   argsList = MethodArgList()
   argsList.append('xData_filename', '', file,
                   'First data set in cvs format')
   argsList.append('yData_filename', '', file,
                   'Second data set in cvs format')
   argsList.append('nbr_correlations', 0, int, 'number of maximised correlations wanted')
   argsList.append('standerdized', False, bool, 'are the two datasets centered and reduced')

   
   def __init__(self,plot=False, nbr_correlations=0, standerdized=False, xData=None, yData=None,xData_filename=None, yData_filename=None, ** kwargs):
      ' Init '
      super(CCA, self).__init__(plot,**kwargs)
      if xData is None:
          if not (xData_filename and isinstance(xData_filename, file)) \
                  or len(xData_filename.name) == 0: raise TypeError("Requires xData_filename to be a file")

      if yData is None:
          if not (yData_filename and isinstance(yData_filename, file)) \
                  or len(yData_filename.name) == 0: raise TypeError("Requires yData_filename to be a file")

      if not(isinstance(nbr_correlations, int))  : raise TypeError("Requires m to be an integer")
      if not(isinstance(standerdized,bool)) : raise TypeError("Requires center to be a boolean")
      #other rule for parameters
      if nbr_correlations< 0 : raise ValueError("Requires m to be positive or greater than 0")

      if isinstance(xData_filename, file):
          xData = pd.DataFrame.from_csv(xData_filename)

      if isinstance(yData_filename, file):
          yData = pd.DataFrame.from_csv(yData_filename)

      if not (isinstance(xData, pd.DataFrame)): raise TypeError("Requires xData to be a panda dataframe")
      if not (isinstance(yData, pd.DataFrame)): raise TypeError("Requires yData to be a panda dataframe")

      self._xData = xData
      self._yData = yData
      self._nbr_correlations=nbr_correlations
      self._standerdized=standerdized
      self.lx = None
      self.ly = None

      return

      
   def vector_root(self,V):
    l=V.size 
    U=np.array(V,float)
    for i in range(0,l):
        U[i]=sqrt(U[i])
    return U
      
   def inv_vector_root(self,V):
    l=V.size
    U=np.array(V,float)
    for i in range(0,l):
        if(V[i]>0):
            U[i]=1/sqrt(U[i])
        else:
            V[i]=0
    return U      
     
   def cov(self,A,B):
    l,c=A.shape
    aux=1.0/(l-1)
    sigma=aux*np.dot(A.T,B)
    return sigma


   def SVD_CCA(self,S_X,S_Y,S_XY,m):
      D,v_x=eig(S_X)
      D=self.inv_vector_root(D)
      D=diag(D)
      CX=np.dot(np.dot(v_x,D),inv(v_x))
      D,v_y=eig(S_Y)
      D=self.inv_vector_root(D)
      D=diag(D)
      CY=np.dot(np.dot(v_y,D),inv(v_y))
      omega=np.dot(np.dot(CX,S_XY),CY)
      U,D,T=svd(omega,full_matrices=0)
      A=np.dot(CX,U)
      A=A[:,:m]
      B=np.dot(CY,T.T)
      B=B[:,:m]
      D=D[0:m]
      D=self.vector_root(D)
      return D,B,A

   def compute(self, signals):
      
      x=self._xData
      y=self._yData

      ' Raise error if parameters are not in the correct type '
      try :
            if not(isinstance(x, pd.DataFrame)): raise TypeError("Requires x to be a pd.DataFrame")
            if not(isinstance(y, pd.DataFrame)): raise TypeError("Requires y to be a pd.DataFrame")
      except TypeError, err_msg:
            raise TypeError(err_msg)
            return
      if not self._standerdized:
            x = Standardize.Standardize(x)
            y = Standardize.Standardize(y)
      x = x.values
      y = y.values
      if self._nbr_correlations == 0:
           self.lx = x.shape[1]
           self.ly = y.shape[1]
           self._nbr_correlations = min(self.lx, self.ly)
      cov_x = self.cov(x, x)
      cov_y = self.cov(y, y)
      cov_xy = self.cov(x, y)
      D,A,B = self.SVD_CCA(cov_x, cov_y, cov_xy, self._nbr_correlations)

      res={}
      res['corr']=D
      res['yWeights']=A
      res['xWeights']=B

      return res


   @staticmethod
   def getArguments():
       return CCA.argsList.getMethodArgs()

   @staticmethod
   def getArgumentsAsDictionary():
       return CCA.argsList.getArgumentsAsDictionary()

