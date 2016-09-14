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

'''----- To be able to import parent directories -----'''
import sys
sys.path.insert(0, '../../src/')

import numpy as np
import importlib

from PlotWindow import PlotWindow

class SynchronyMethod:
    def __init__(self, method_name, method_type, method_data_type, method_signal_type, method_number_user_type, method_description=''):
        
        try : 
            self._method_name = method_name
            self._method_type = self.initMethodType(method_type)
            self._method_data_type = self.initMethodDataType(method_data_type)
            self._method_signal_type = self.initMethodSignalType(method_signal_type)
            self._method_number_user_type = self.initMethodNumberUserType(method_number_user_type)
            self._method_description = method_description
        except ValueError, err :
            raise ValueError(err)
        
     
    def initMethodType(self, method_type) :
        if('Linear' == method_type): 
            out = 0
        elif('Nonlinear' == method_type): 
            out = 1
        elif('MachineLearning' == method_type): 
            out = 2
        elif (0 == method_type) or (1 == method_type) or (2 == method_type):
            out = method_type
        else:
            raise ValueError("method_type must be a positive integer:0,1 or 2 or a string : Linear, Nonlinear or MachineLearning")
        return out
    
    
    def initMethodDataType(self, method_data_type) :
        if('Continuous' == method_data_type): 
            out = 0
        elif('Categorical' == method_data_type): 
            out = 1
        elif (0 == method_data_type) or (1 == method_data_type):
            out = method_data_type
        else:
            raise ValueError("method_data_type must be a positive integer:0 or 1 or a string : Continuous or Categorical")  
        return out    
    
    
    def initMethodSignalType(self, method_signal_type) :
        if('Monovariate' == method_signal_type): 
            out = 0
        elif('Multivariate' == method_signal_type): 
            out = 1
        elif (0 == method_signal_type) or (1 == method_signal_type):
            out = method_signal_type
        else:
            raise ValueError("method_signal_type must be a positive integer:0 or 1 or a string : Monovariate or Multivariate")
        return out
    
    
    def initMethodNumberUserType(self, method_number_user_type) :
        if('DataFrom2Persons' == method_number_user_type): 
            out = 0
        elif('DataFromManyPersons' == method_number_user_type): 
            out = 1
        elif (0 == method_number_user_type) or (1 == method_number_user_type):
            out = method_number_user_type
        else:
            raise ValueError("method_number_user_type must be a positive integer:0 or 1 or a string : DataFrom2Persons or DataFromManyPersons")
        return out
    
    
    def defineConstructorParameters(self, method_parameters) :
        available_type = [bool, int, float, str]
        
        for key in method_parameters.keys():
            if method_parameters[key] == 'bool' :
                method_parameters[key] = bool
            if method_parameters[key] == 'int' :
                method_parameters[key] = int
            if method_parameters[key] == 'float' :
                method_parameters[key] = float
            if method_parameters[key] == 'str' :
                method_parameters[key] = str
        

        if isinstance(method_parameters, dict) :
            isTypeOk = True
            for value in method_parameters.values():
                if not(value in available_type) :
                    isTypeOk =  False
                    raise ValueError("method_parameters type " + value + " is not an available type (bool, int, float or str)")
                    
            if isTypeOk :
                self._method_constructor_parameters = method_parameters
            else :
                out = -1           
        else :
            raise ValueError("method_parameters must be a a dictionary (key=parameter name, value=parameter type)")
            out = -1
    
    
    def defineParametersDescriptions(self, method_parameters_description) :
        
        if isinstance(method_parameters_description, dict) :
            self._method_parameters_description = method_parameters_description  
        else :
            raise ValueError("method_parameters must be a a dictionary (key=parameter name, value=parameter type)")
            out = -1
            
        
    def importMethodModule(self):
        module_str = ""
        #Define parent package
        if self._method_number_user_type == 0 :
            module_str += "DataFrom2Persons"
        else :
            module_str += "DataFromManyPersons"
        module_str += "."
        if self._method_signal_type == 0 :
            module_str += "Monovariate"
        else :
            module_str += "Multivariate"
        module_str += "."
        if self._method_data_type == 0 :
            module_str += "Continuous"
        else :
            module_str += "Categorical"     
        module_str += "."
        if self._method_type == 0 :
            module_str += "Linear"
        elif self._method_type == 1 :
            module_str += "Nonlinear"
        else :
            module_str += "MachineLearning"
        module_str += "."
        
        module_str += self._method_name

        # import the module
        try :
            self._method_module = importlib.import_module(module_str)
        except Exception, e :
            raise Exception("Exception in import of module " + module_str + " :\n" + str(e))
        self._module_full_name = module_str
        
    
    def initMethod(self, method_parameters_values) :
        # Get the class name
        try : 
            self._method_class = getattr(self._method_module, self._method_name)
        except AttributeError, err :
            raise AttributeError("Cannot find class " + self._method_name + " in module : " + self._module_full_name)
        
        # Call constructor
        try : 
            self._method_instance = self._method_class(**method_parameters_values)
        except TypeError, err_msg :
            raise TypeError("TypeError in constructor of class " + self._method_name + ":\n" + str(err_msg))
        except ValueError, err_msg :
            raise ValueError("ValueError in constructor of class " + self._method_name + ":\n" + str(err_msg))
        except Exception, e :
            raise Exception("Exception in constructor of class " + self._method_name + " : " + str(e))
        
    
    def computeMethod(self, method_signals) :
        # Get compute method
        try :
            self._method_compute = getattr(self._method_class, "compute")
        except AttributeError, err :
            raise AttributeError("Cannot find compute() method of class : " + self._method_name)
       
        # Insert the instance in input parameters list
        method_signals.insert(0, self._method_instance)

        #Compute the method
        try :
            self._compute_result = getattr(self._method_class, "compute")(*method_signals)
        except AttributeError, err_msg :
            raise AttributeError("Cannot find compute() method of class : " + self._method_name)
        except TypeError, err_msg:
            raise TypeError("TypeError in compute() :\n" + str(err_msg))
        except ValueError, err_msg:
            raise ValueError("ValueError in compute() :\n" + str(err_msg))
        except Exception, e :
            raise Exception("Exception in compute() :\n" + str(e))
        
        return True
    
    
    def visualizeResult(self) :         
        # Get plot method
        try :
            self._method_plot = getattr(self._method_class, "plot")
        except AttributeError, err :
            raise AttributeError("Cannot find plot() method of class : " + self._method_name)
        
        try : 
            self._plot_result = self._method_plot(self._method_instance)
        except Exception, e :
            raise Exception("Exception in plot() :\n" + str(e))

        figure = PlotWindow()
        figure.plot_figure(self._plot_result)
        

            

        
        
        
    