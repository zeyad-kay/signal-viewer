import numpy as np
import pyedflib

def read_file(filename):
    f= pyedflib.EdfReader(filename)
    label = f.getSignalLabels()[0]
    freq = f.getSampleFrequency(0)
    samples = f.readSignal(0)
    time = np.linspace(0,samples.__len__() * 1/freq,samples.__len__())
    return {
        "x":time,
        "y":samples,
        "label":label
    }