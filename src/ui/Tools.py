import matplotlib.pyplot as plot
import numpy as np
from os.path import basename


class Tools:
    @staticmethod
    def plotSignals(signals, files, names):
        nbNames = len(names)
        nbFiles = len(files)

        if nbNames < 1 or nbFiles < 1:
            return

        nSignals = len(signals)

        #figureName = basename(fileName) + " - " + names

        plot.ion()
        f, axarr = plot.subplots(nbNames, nbFiles)
        f.canvas.set_window_title('Input signals')
        #
        # colors = "bgrcmyk"

        maxSignalLen = 250000

        for i in xrange(0, nbNames-1):
            time = signals[i].index
            timelabel = signals[i].index.names[0].encode("utf-8")
            for j in xrange(0, nbFiles-1):
                axarr[i, j].set_title(names[i])
                axarr[i, j].set_xlabel(timelabel)
                axarr[i, j].plot(time, signals[i+j], label=names[i])
                axarr[i, j].legend(loc='best')

            # l = len(signals[i])
            # print l
            # if(l > maxSignalLen):
            #     print "Warning: signal "+names[i]+" too large to plot, decimating to preview"
            #     decimation_factor = l/maxSignalLen
            #     s = signals[i]
            #     s = np.max(s.reshape(-1,decimation_factor),axis=1)
            #     plot.figure(names[i])
            #     plot.plot(time, s, label=names[i])
            # else:
            #     plot.figure(names[i])
            #     plot.plot(time, signals[i], label=names[i])
            #plot.figure(figureName)

        # plot.show()


    @staticmethod
    def plotOneSignal(signal, name, fileName=""):
        time = []

        maxSignalLen = 250000

        time = signal.index
        timelabel = signal.index.names[0].encode("utf-8")

        plot.ion()

        figureName = basename(fileName) + " - " + name

        l = len(signal)
        if(l > maxSignalLen):
            print "Warning: signal "+name+" too large to plot, decimating to preview"
            decimation_factor = l/maxSignalLen
            print decimation_factor
            s = signal.as_matrix()
            s = np.max(s.reshape(-1,decimation_factor),axis=1)
            t = time.values
            t = np.max(t.reshape(-1,decimation_factor),axis=1)
            plot.figure(figureName)
            plot.plot(t, s, label=name)
        else:
            plot.figure(figureName)
            plot.plot(time, signal, label=name)

        #plot.show()
