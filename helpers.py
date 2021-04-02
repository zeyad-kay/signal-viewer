import numpy as np
import pyedflib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def read_edf(filename):
    """
    Return a dictionary containing the samples, time, frequency, and label
    of an EDF file.
    """
    f= pyedflib.EdfReader(filename)
    label = f.getSignalLabels()[0]
    freq = f.getSampleFrequency(0)
    samples = f.readSignal(0)
    time = np.linspace(0,samples.__len__() * 1/freq,samples.__len__())
    return {
        "x":time,
        "y":samples,
        "freq": freq,
        "label":label
    }

def save_pdf(filename,plots=[]):
    """
    Write a PDF file of the plots and their spectrograms.
    """
    with PdfPages(filename + ".pdf") as pdf:
        fig,axs = plt.subplots(ncols=2,nrows=plots.__len__(),constrained_layout=True)

        if plots.__len__() == 1:
            axs = np.array([axs])

        for i,plot in enumerate(plots):
            # Take only 1000 samples
            axs[i][0].plot(plot["x"][:1000],plot["y"][:1000])
            axs[i][0].set_title(plot["label"])
            
            axs[i][1].specgram(plot["y"],plot["freq"])
            axs[i][1].set_title(plot["label"] + " " + "Spectrogram")
        
        pdf.savefig()