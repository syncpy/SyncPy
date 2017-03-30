# -*- coding: UTF-8 -*-
import multiprocessing
import tempfile

import matplotlib.pyplot as plt
import pickle
import sys
from ctypes import c_char_p
import os
import csv
import numpy as np
import copy

def debug(farg, *args):
    pass
    #print farg
    #for arg in args:
    #   print arg

def isType(object, typeName):
    return type(object) is typeName

class MethodArg:
    def __init__(self, label, value, type, hint):
        self.label = label
        self.value = value
        self.type = type
        self.hint = hint

    def __repr__(self):
        return "{0}, {1}, {2}, {3}".format(self.label, self.type, self.value, self.hint)


class MethodArgList:
    def __init__(self):
        self.MethodArgs = []

    def append(self, label, value, type, hint):
        self.MethodArgs.append(MethodArg(label, value, type, hint))

    def getMethodArgs(self):
        return self.MethodArgs

    def getArgumentsAsDictionary(self):
        values = dict()
        for arg in self.MethodArgs:
            values[arg.label] = arg.value
        return values

    def size(self):
        return len(self.MethodArgs)

class Method(multiprocessing.Process):
    """Parent Method"""
    #results = multiprocessing.Queue(0)
    errorRaised = False

    def __init__(self, plot):
        multiprocessing.Process.__init__(self)
        #print self.__doc__
        self.signals = None
        self._plot = plot
        self.res = {}
        self.tmpRes = None
        self.resQueue = None
        self.results = None
        self.outputFilename = None

    def setOutputFilename(self, filename):
        self.outputFilename = filename

    def start(self, signals, queue):
        self.resQueue = queue
        self.signals = signals
        super(Method, self).start()

    def compute(self, signals):
        pass

    def run(self):
        self.tmpRes = None
        self.errorRaised = False
        try:
            debug("Computing starts")
            self.results = self.compute(self.signals)
            self.tmpRes = self.results
            debug("Computing ends")

        except Exception, e:
            print "Computing error: %s" % e.message
            self.tmpRes = str(e.message)
            self.errorRaised = True

        if True or len(self.tmpRes) > 10:
            debug("Result is long")
            f = tempfile.TemporaryFile(prefix="Syncpy-"+self.name, delete=False)
            pickle.dump(self.tmpRes, f)
            self.tmpRes = f.name

        for i in plt.get_fignums():
            debug("Putting fig in queue : %d"% i)
            f = plt.figure(i)
            pickle.dump(f, file('tmp%d.plot' % i, 'w'))

        debug("Putting in queue : ", self.tmpRes)

        self.resQueue.put(self.errorRaised)
        self.resQueue.put(self.tmpRes)

        debug("Writing results starts")
        self.writeToCSV(self.results)
        debug("Writing results ends")

    def plot(self):
        if self._plot == True:
            plt.ion()
            self.plot_result()

    def plot_result(self):
        pass

    def writeToCSV(self, results):
        if results != None:
            keys = results.keys()
            filteredKeys = [k for k in keys if type(results[k]) is np.ndarray and results[k].size > 1 ]
            filteredResults = dict()
            for k in filteredKeys:
                filteredResults[k] = results[k]
            if len(filteredResults) > 0:
                rows = zip(*filteredResults.values())
                with open(self.outputFilename, 'wb') as f:
                    writer = csv.writer(f)
                    for key in filteredKeys:
                        if keys.index(key) > 0:
                            f.write(',')
                        f.write(key)
                    f.write(os.linesep)
                    writer.writerows(rows)

    def getFigures(self):
        return self.figArray

    @staticmethod
    def getArguments():
        return []

    @staticmethod
    def getArgumentsAsDictionary():
        return []
