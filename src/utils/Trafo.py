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

import numpy as np
import pandas as pd


def Trafo(signal, sk, trafo_type, log_base=2):
    """
    It transforms a monovariate/multivariate signals (in pandas DataFrame format) in a new signal
    by applying a square root or logaritmic or inverse transformation.
    
    :param signal:
        input signal
    :type signal: pd.DataFrame
    
    :param sk:
        {'pos','neg'} the skewness of signal distribution. 
    :type sk: str
    
    :param trafo_type:
        {'sqrt','log','inv'} the kind of tranformation should be applied 
    :type trafo_type: str

    :param log_base:
        The base of the log. Available options:
            1. 2.0;
            2. np.e; and
            3. 10.0.
        Default: 2
        
    :type log_base: int
    
    :returns: pd.DataFrame
            -- transformed signal
    """
    
    ' Raise error if parameters are not in the correct type '
    if not(isinstance(signal, pd.DataFrame)) : raise TypeError("Requires signal to be a pd.DataFrame")
    if not(isinstance(sk, str))     : raise TypeError("Requires sk to be a string")
    if not(isinstance(trafo_type, str))      : raise TypeError("Requires trafo_type to be a string")
    if not(isinstance(log_base, float))     : raise TypeError("Requires log_base to be a float")

        
    ' Raise error if parameters do not respect input rules '
    if sk!='pos' and sk!='neg' : raise ValueError("Requires sk to be 'pos' or 'neg'")
    if trafo_type!='sqrt' and trafo_type!='log' and trafo_type!='inv': raise ValueError("Requires trafo_type to be 'sqrt' or 'log' or 'inv'")
    if log_base!=2.0 and log_base!=np.e and log_base!=10.0 : raise ValueError("Requires log_base to be 2.0 or np.e or 10.0" )
    
    if sk == 'pos':
        if trafo_type == 'sqrt':
            pr_col=(signal<1).any()
        
            if np.sum(pr_col)!=0:
                signal.iloc[:,pr_col.values==True]=signal.iloc[:,pr_col.values==True]-signal.min()+1.0
        
            signal_sqrt=signal.apply(np.sqrt)
        
            return (signal_sqrt)
        
        elif trafo_type == 'log':
    
            pr_col=(signal<1).any()
        
            if np.sum(pr_col)!=0:
                signal.iloc[:,pr_col.values==True]=signal.iloc[:,pr_col.values==True]-signal.min()+1.0
        
            if log_base==np.e:
                signal_log=signal.apply(np.log)
            elif log_base==2:
                signal_log=signal.apply(np.log2)
            elif log_base==10:
                signal_log=signal.apply(np.log10)
            
            return (signal_log)
        
        elif trafo_type == 'inv':
            pr_col=(signal<1).any()
            signal=signal*(1.0)
            
            if np.sum(pr_col)!=0:
                signal.iloc[:,pr_col.values==True]=(signal.iloc[:,pr_col.values==True]-(signal.iloc[:,pr_col.values==True]).min()+1.0)
                signal.iloc[:,pr_col.values==True]=1-signal.apply(np.reciprocal)+signal.min()
                
                signal.iloc[:,pr_col.values==False]=1-(signal.iloc[:,pr_col.values==False]).apply(np.reciprocal)+(1-(signal.iloc[:,pr_col.values==False]).apply(np.reciprocal)).min().values
  
            return (signal)
        
    elif sk == 'neg':
        if trafo_type=='sqrt':
            signal_=(-1.0)*signal   
            signal_sqrt=(((signal_-signal_.min()+1.0).apply(np.sqrt).max())+1).values-(signal_+(-signal_.min()+1.0).values).apply(np.sqrt)
            return(signal_sqrt)
        
        elif trafo_type=='log':            
            signal_=(-1.0)*signal
            
            #print (-signal_.min()+1.0).values
            #print ((-1.0)*((signal_+(-signal_.min()+1.0).values).apply(np.log)).max()-1.0).values
            
            if log_base==np.e:
                signal_log=-(signal_+(-signal_.min()+1.0).values).apply(np.log)-((-1.0)*((signal_+(-signal_.min()+1.0).values).apply(np.log)).max()-1.0).values
            elif log_base==2:
                signal_log=signal.apply(np.log2)
            elif log_base==10:
                signal_log=signal.apply(np.log10)
                
            return (signal_log)
        
        elif trafo_type=='inv':
            signal_=(-1.0)*signal
            
            print (-signal_.min()+1.0).values
            print ((-1.0)*((signal_+(-signal_.min()+1.0).values).apply(np.reciprocal)).min()+1.0).values

            tmpvalues = (signal_+(-signal_.min()+1.0).values)
            try :
                if np.any(tmpvalues == 0) : raise ValueError("Divide by zero exception : (signal_+(-signal_.min()+1.0).values) = 0")
            except ValueError, err_msg:
                raise ValueError(err_msg)
                return

            signal_inv=1.0/tmpvalues+((-1.0)*((signal_+(-signal_.min()+1.0).values).apply(np.reciprocal)).min()+1.0).values
            
            return (signal_inv)

