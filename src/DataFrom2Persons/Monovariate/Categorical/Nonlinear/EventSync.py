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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from   math import sqrt


class EventSync:
   """
   It computes synchronicity (Q) and time delay patterns (q) between two monovariate signals x and y
   (in pandas DataFrame format) in which events can be identified.  
   
   **Reference :**
   
   * R.Quian Quiroga; T.Kreuz and P.Grassberger; "A simple and fast method to measure synchronicity and time delay patterns." (Phys.Rev. E; 66; 041904 (2002))
   
   :param atype:
       it can assumes the following values: 'tot', 'tsl', 'asl' \n
         1. 'tot': synchronicity (Q) and time delay pattern(q) are computed over all the time signals
         2. 'tsl': time resolved variants of Q and q\n
         3. 'asl': averaged time resolved variants of Q and q over a window whose size is specified by the window parameter
       Default: 'tot
   :type atype: str
   
   :param tau:
      it is a binary value [0,1] indicating which type of algorithm is used to estimates the delay. \n
         1. 0 : a prefixed tau with value specified by lag_tau will be used. It should be smaller than half the minimum interevent distance
         2. 1 : an atuomatically estimated local tau for each pair of events in the series will be used. The local tau for a generic pair of events i and j is computed as the half of the minimum value in the following set
      [tau_x(i+1)- tau_x(i); tau_x(i)-tau_x(i-1); tau_y(j+i)-tau_y(j), tau_y(j)-tau_y(j-1)]
      Default: 1
   :type tau: int
   
   :param lag_tau:
      it is the (positive) number of samples will be used as delay when tau is set to 0
   :type lag_tau: int
   
   :param window:
      it is the size of the window (in samples) used to compute Q and q when type is 'asl'.
   :type window: int
   
   :param plot:
      if True the plot of Q and q is returned when atype is set to 'tsl' or 'asl'. Default: False
   :type plot: bool 
   """
        
        
   def __init__(self, atype='tot', tau=0, lag_tau=0, window=1, plot=False):
      
      ' Raise error if parameters are not in the correct type '
      try :
          if not(isinstance(atype, str))    : raise TypeError("Requires type to be a string")
          if not(isinstance(tau, int))     : raise TypeError("Requires tau to be an integer")
          if not(isinstance(lag_tau, int)) : raise TypeError("Requires lag_tau to be an integer")
          if not(isinstance(window, int))  : raise TypeError("Requires window to be an integer")
          if not(isinstance(plot, bool))   : raise TypeError("Requires plot to be a boolean")
      except TypeError, err_msg:
          raise TypeError(err_msg)
          return
      
      ' Raise error if parameters do not respect input rules '
      try : 
         if atype != 'tot' and  atype != 'tsl' and  atype != 'asl' :
           raise ValueError("Requires type to be have these values : {'tot', 'tsl', 'asl'}")
         if tau != 0  and tau != 1 : raise ValueError("Requires tau to be to be 1 or 2")
         if lag_tau < 0           : raise ValueError("Requires lag_tau to be a positive scalar inferior to window length" )
      except ValueError, err_msg:
         raise ValueError(err_msg)
         return
         
      self.atype = atype
      self.tau = tau
      self.lag_tau = lag_tau
      self.window = window
      self._plot = plot


   def heaviside(self,x):
      """
      It computes the heaviside function of x
      
      :param x:
         number on which computing heaviside
      :type x: int 
      
      :returns: int
            -- heaviside function value
      """
      if x <= 0:
         res = 0.0
      else :
         res = 1
      
      return res
            
            
   def plot(self):
      """
        It plots the resulting Q and q when atype is set to 'tsl' or 'asl'
        
        :returns: plt.figure 
               -- figure plot
      """
       
      x=np.arange(0, self.Qout.size, 1)

      figure, axarr = plt.subplots(2, sharex=True)
      axarr[0].set_title('Synchrony and time delay pattern')
      axarr[0].set_xlabel('Samples')
      axarr[1].set_xlabel('Samples')
      axarr[0].set_ylim(0,np.nanmax(self.Qout))
      axarr[0].plot(x, self.Qout, label="Synchrony (Qn)")
      axarr[1].set_ylim(np.nanmin(self.qout),np.nanmax(self.qout))
      axarr[1].plot(x, self.qout, label="Time delay pattern (qn)")
      axarr[0].legend(loc='best')
      axarr[1].legend(loc='best')
      
      return figure
      
      
   def optimal_tau(self,t_peak_x,t_peak_y):
      """
      It estimates the value of tau as the half the minimum of all the intervent distances.
      
      :param t_peak_x:
         sequences of events in x
      :type t_peak_x: array
      
      :param t_peak_y:
         sequences of events in y
      :type t_peak_y: array
      
      :returns: array
            -- optimal value for tau
      """
 
      if self.tau==1:
          lag_tau_array=np.zeros((len(t_peak_x),len(t_peak_y)),dtype=np.int)
           
          for ix in range(0,len(t_peak_x)):
              for iy in range(0,len(t_peak_y)):
                  if ix==0:
                      if iy==0:
                          lag_tau_loc=min((t_peak_x[ix+1]-t_peak_x[ix]),(t_peak_y[iy+1]-t_peak_y[iy]))/2.0
                          lag_tau_array[ix,iy]=lag_tau_loc
                       
                      elif (iy >0) and (iy<(len(t_peak_y)-1)):
                          lag_tau_loc=min((t_peak_x[ix+1]-t_peak_x[ix]),(t_peak_y[iy+1]-t_peak_y[iy]),(t_peak_y[iy]-t_peak_y[iy-1]))/2.0
                          lag_tau_array[ix,iy]=lag_tau_loc
                   
                      elif iy==len(t_peak_y)-1:
                          lag_tau_loc=min((t_peak_x[ix+1]-t_peak_x[ix]),(t_peak_y[iy]-t_peak_y[iy-1]))/2.0
                          lag_tau_array[ix,iy]=lag_tau_loc
                               
                  elif (ix>0) and (ix<(len(t_peak_x)-1)):
                      if iy==0:
                           lag_tau_loc=min((t_peak_x[ix+1]-t_peak_x[ix]),(t_peak_x[ix]-t_peak_x[ix-1]),(t_peak_y[iy+1]-t_peak_y[iy]))/2.0
                           lag_tau_array[ix,iy]=lag_tau_loc
                           
                      elif (iy >0) and iy<((len(t_peak_y)-1)):
                           lag_tau_loc=min((t_peak_x[ix+1]-t_peak_x[ix]),(t_peak_x[ix]-t_peak_x[ix-1]),(t_peak_y[iy+1]-t_peak_y[iy]),(t_peak_y[iy]-t_peak_y[iy-1]))/2.0
                           lag_tau_array[ix,iy]=lag_tau_loc
                   
                      elif iy==len(t_peak_y)-1:
                           lag_tau_loc=min((t_peak_x[ix+1]-t_peak_x[ix]),(t_peak_x[ix]-t_peak_x[ix-1]),(t_peak_y[iy]-t_peak_y[iy-1]))/2.0
                           lag_tau_array[ix,iy]=lag_tau_loc
               
                  elif ix==len(t_peak_x)-1:
                      if iy==0:
                           lag_tau_loc=min((t_peak_x[ix]-t_peak_x[ix-1]),(t_peak_y[iy+1]-t_peak_y[iy]))/2.0
                           lag_tau_array[ix,iy]=lag_tau_loc

                      elif (iy >0) and iy<(len(t_peak_y)-1):
                           lag_tau_loc=min((t_peak_x[ix]-t_peak_x[ix-1]),(t_peak_y[iy+1]-t_peak_y[iy]),(t_peak_y[iy]-t_peak_y[iy-1]))/2.0
                           lag_tau_array[ix,iy]=lag_tau_loc
           
                      elif iy==len(t_peak_y)-1:
                           lag_tau_loc=min((t_peak_x[ix]-t_peak_x[ix-1]),(t_peak_y[iy]-t_peak_y[iy-1]))/2.0
                           lag_tau_array[ix,iy]=lag_tau_loc
       
          return lag_tau_array



   def Jfunct(self,peak_x, peak_y):
      """
      It computes the terms of the conditional probabilities c_tau
      
      :param peak_x:
         peaks in x
      :type peak_x: array
      
      :param peak_y:
         peaks in y
      :type peak_y: array
      
      :returns: tuple
            -- terms of the conditional probabilities c_tau
      """
      t_peak_x=np.array(list(peak_x.index.values))
      t_peak_y=np.array(list(peak_y.index.values))
      
      #computation of Jij
      jay_out_xy=np.zeros((peak_x.shape[0],peak_y.shape[0]))
      for px in range(0,peak_x.shape[0]):
          for py in range(0,peak_y.shape[0]):
              dt=t_peak_x[px] - t_peak_y[py]
              
              if self.tau==0:
                  if (dt>0) and (dt<=self.lag_tau):
                      jay_out=1
                  elif dt==0:
                      jay_out=0.5
                  else:
                      jay_out=0
               
              elif self.tau==1:
                  if (dt>0) and (dt<=self.lag_tau[px][py]):
                      jay_out=1
                  elif dt==0:
                      jay_out=0.5
                  else:
                      jay_out=0
          
              jay_out_xy[px,py]=jay_out
   
      #computation of Jji
      jay_out_yx=np.zeros((peak_y.shape[0],peak_x.shape[0]))
      for py in range(0,peak_y.shape[0]):
          for px in range(0,peak_x.shape[0]):
              dt=t_peak_y[py] - t_peak_x[px]
                   
              if self.tau==0:
                  if (dt>0) and (dt<=self.lag_tau):
                      jay_out=1
                  elif dt==0:
                      jay_out=0.5
                  else:
                      jay_out=0
  
              elif self.tau==1:
                  if (dt>0) and (dt<=self.lag_tau[px][py]):
                      jay_out=1
                  elif dt==0:
                      jay_out=0.5
                  else:
                      jay_out=0
                      
              jay_out_yx[py,px]=jay_out
  
      return (jay_out_xy,jay_out_yx)


   def Qq_tot(self,jay_out_xy,jay_out_yx,l_peak_x,l_peak_y):
      """
      It computes synchronicity (Q) and time delay pattern(q) over all the time series ('tot' type)
      
      :param jay_out_xy:
         Jfunct for x given y
      :type jay_out_xy: array
      
      :param jay_out_yx:
         Jfunct for y given x
      :type jay_out_yx: array
      
      :param l_peak_x:
         peaks locations in x
      :type l_peak_x: array
      
      :param l_peak_y:
         peaks locations in y
      :type l_peak_y: array
      
      :returns: tuple
            -- Q and q over the whole length time series
      """
      c_xy=np.sum(jay_out_xy)
      c_yx=np.sum(jay_out_yx)
      
      
      Q_tau=(c_xy + c_yx)/sqrt(l_peak_x*l_peak_y)
      q_tau=(c_yx - c_xy)/sqrt(l_peak_x*l_peak_y)
       
      return (Q_tau,q_tau)


   def QQ_tsl(self,jay_out_xy,jay_out_yx,lx,peak_x,peak_y, delta_sample):
      """
      It computes synchronicity (Q) and time delay pattern (q) when atype is set to 'tsl' or
      to 'asl' 
      
      :param jay_out_xy:
         Jfunct for x given y
      :type jay_out_xy: array
      
      :param jay_out_yx:
         Jfunct for y given x
      :type jay_out_yx: array
      
      :param peak_x:
         peaks locations in x
      :type peak_x: array
      
      :param peak_y:
         peaks locations in y
      :type peak_y: array
      
      :param delta_sample:
         size of window (useful only for computing Q and q in 'asl') 
      :type delta_sample: array
      
      :returns: tuple
            -- Q and q over the whole length time series
      """
      '''
      t_peak_x=np.array(list(peak_x.index.values))
      t_peak_y=np.array(list(peak_y.index.values))
      '''
      
      # Arrange peaks indexes location in an array
      t_peak_x = peak_x.iloc[:,1].values
      t_peak_y = peak_y.iloc[:,1].values
      
      jay_fincnxy=np.zeros((1,lx))[0]
             
      for px in range(0,peak_x.shape[0]):
          for py in range(0,peak_y.shape[0]):
              jay=np.array([])
              for sample in range(0,lx):
                  tmp=jay_out_xy[px][py]*self.heaviside(sample-delta_sample-t_peak_x[px])
                  if (np.isnan(tmp)):
                      tmp=0
                  jay=np.append(jay,tmp)       
              jay_fincnxy=jay_fincnxy+jay
               
      jay_fincnyx=np.zeros((1,lx))[0]
      
      for py in range(0,peak_y.shape[0]):
          for px in range(0,peak_x.shape[0]):
              jay=np.array([])
              for sample in range(0,lx):
                  tmp=jay_out_yx[py][px]*self.heaviside(sample-delta_sample-t_peak_y[py])
                  if (np.isnan(tmp)):
                      tmp=0
                  jay=np.append(jay,tmp)
                               
              jay_fincnyx=jay_fincnyx+jay
      
      Qn=jay_fincnyx+jay_fincnxy
      qn=jay_fincnyx-jay_fincnxy
       
      return(Qn,qn)

   def compute(self, x, y):
      """
      It computes the wanted version of Q and q
      
      :param x:
          first input signal
      :type x: pd.DataFrame
        
      :param y:
          second input signal
      :type y: pd.DataFrame
      
      :returns: dict 
              -- Q, q
      """
      
      ' Raise error if parameters are not in the correct type '
      try :
          if not(isinstance(x, pd.DataFrame)) : raise TypeError("Requires x to be a pd.DataFrame")
          if not(isinstance(y, pd.DataFrame)) : raise TypeError("Requires y to be a pd.DataFrame")
      except TypeError, err_msg:
          raise TypeError(err_msg)
          return
         
      ' Raise error if x and y have not the same size'
      try :
         if x.shape[0] != y.shape[0] :
            raise ValueError("x and y signals must have same size")
      except ValueError, err_msg:
         raise ValueError(err_msg)
         return

      # Add a column 'index' to save indexes of peaks 
      x['index'] = range(0,x.shape[0])
      y['index'] = range(0,y.shape[0])
      
      ones_x=x.iloc[:,0]==1
      ones_y=y.iloc[:,0]==1
      
      peak_x=x.loc[ones_x]
      peak_y=y.loc[ones_y]
      
      l_peak_x=peak_x.shape[0]
      l_peak_y=peak_y.shape[0]
       
      t_peak_x=np.array(list(peak_x.index.values))
      t_peak_y=np.array(list(peak_y.index.values))
      
      if  (l_peak_x>1) and (l_peak_y>1):
          diff_t_peak_x=np.diff(t_peak_x)
          diff_t_peak_y=np.diff(t_peak_y)
          min_diff_x=np.min(diff_t_peak_x)
          min_diff_y=np.min(diff_t_peak_y)
          
          min_diff=(min(min_diff_x, min_diff_y) / 2)
          
      elif ((l_peak_x<=1) and (l_peak_y>1)) or ((l_peak_y<=1) and (l_peak_x>1)) or ((l_peak_x<=1) and (l_peak_y<=1)):
         ' Raise warnings '
         raise Warning("only two or none events in the times series!")    
      
      if self.tau==0:
         try :
            if self.lag_tau >= min_diff :
                raise ValueError("lag_tau should be smaller than this value %d: " %min_diff)
         except ValueError, err_msg:
            raise ValueError(err_msg)
            return
      
      if self.tau==1:
          self.lag_tau=self.optimal_tau(t_peak_x,t_peak_y)

        
      if self.atype=='tot':
          [jay_out_xy,jay_out_yx]=self.Jfunct(peak_x,peak_y)
          [self.Qout,self.qout] = self.Qq_tot(jay_out_xy,jay_out_yx,l_peak_x,l_peak_y)
       
      elif self.atype=='tsl':
         delta_sample=0
         lx=x.shape[0]
          
         [jay_out_xy,jay_out_yx]=self.Jfunct(peak_x,peak_y)
          
         [self.Qout, self.qout]=self.QQ_tsl(jay_out_xy,jay_out_yx,lx,peak_x,peak_y,delta_sample)

      elif self.atype=='asl':
         delta_sample=0
         lx=x.shape[0]
         
         [jay_out_xy,jay_out_yx]=self.Jfunct(peak_x,peak_y)
         
         [Qn,qn]=self.QQ_tsl(jay_out_xy,jay_out_yx,lx,peak_x,peak_y,delta_sample)
         
         delta_sample=self.window
         [Qn_deltan,qn_deltan]=self.QQ_tsl(jay_out_xy,jay_out_yx,lx,peak_x,peak_y,delta_sample)
          
         delta_x=pd.rolling_sum(x,delta_sample, center=False) 
         delta_y=pd.rolling_sum(y,delta_sample, center=False) 
         
         delta_x=delta_x.iloc[:,0].values
         delta_y=delta_y.iloc[:,0].values
                  
         delta_Q=Qn-Qn_deltan
         delta_q=qn-qn_deltan

         delta_events=np.sqrt(delta_x*delta_y)
         
         self.Qout = (1.0)*delta_Q/delta_events
         self.qout = (1.0)*delta_q/delta_events
         
         self.Qout[np.isinf(self.Qout)] = np.nan
         self.qout[np.isinf(self.qout)] = np.nan
      
      if self._plot==True:
          plt.ion()
          self.plot()
      
      
      res={}
      res['Q']=self.Qout
      res['q']=self.qout
      
      return res








