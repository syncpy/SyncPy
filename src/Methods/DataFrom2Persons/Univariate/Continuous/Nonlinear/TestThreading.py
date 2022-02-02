import sys
import time
import numpy as np

sys.path.insert(0, '../src/')

from Method import Method, MethodArgList

class TestThreading(Method):
    """
    This is just a Test Module
    """
    argsList = MethodArgList()
    argsList.append('timeToSleep', 2, int, 'seconds to sleep')
    argsList.append('plot', False, bool, 'plot or not')
    argsList.append('type', ['menu1','menu2','menu3'], list, 'menu test')


    ''' Constuctor '''
    def __init__(self, timeToSleep, plot, type, **kwargs):
        ' Raise error if parameters are not in the correct type '
        #Method.__init__(self)
        super(TestThreading, self).__init__(plot,**kwargs)

        self.timeToSleep=timeToSleep
        self.type = type

    def compute(self, signals):
        try :
            if not(isinstance(self.timeToSleep, int)) : raise TypeError("Requires time to be an integer")
        except TypeError as err_msg:
            self.errorRaised = True
            return "Error: "+str(err_msg)

        ' Raise error if parameters do not respect input rules '
        try :
            if self.timeToSleep <= 0 : raise ValueError("Requires time to be a positive integer different from 0")
        except ValueError as err_msg:
            self.errorRaised = True
            return "Error: "+str(err_msg)

        print (self.timeToSleep)
        print (self.plot)
        print (self.type)

        count = 0
        x = signals[0]
        y = signals[1]
        while count < self.timeToSleep:
            try:
                time.sleep(1)
                count += 1
            except Exception as e:
                self.errorRaised = True
                return "Error: "+str(e)
        res = []
        res.append(count)
        res.append("toto")
        return res

    @staticmethod
    def getArguments():
        return TestThreading.argsList.getMethodArgs()

    @staticmethod
    def getArgumentsAsDictionary():
        return TestThreading.argsList.getArgumentsAsDictionary()
