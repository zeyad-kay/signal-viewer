import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.io.wavfile import read,write
import pyedflib

def read_edf(filename):
    """
    Return a dictionary containing the samples, time, frequency, and label
    of an EDF file.
    """
    f= pyedflib.EdfReader(filename)
    label = f.getSignalLabels()[0]
    Fs = f.getSampleFrequency(0)
    samples = f.readSignal(0)
    return {
        "samples":samples,
        "N":len(samples),
        "Fs": Fs,
        "label":label
    }

def save_wav(filename,rate,samples):
    write(filename,rate,samples.astype(np.int16))

def read_wav(filename):
    Fs,data=read(filename)
    samples = data
    label = filename.split("/")[-1][:-4]
    return {
        "Fs":Fs,
        "samples":samples,
        "N":len(samples),
        "label":label
    }

def save_pdf(filename,signal,time,equalized_samples):
    """
    Write a PDF file of the plots and their spectrograms.
    """
    with PdfPages(filename + ".pdf") as pdf:
        fig,axs = plt.subplots(ncols=2,nrows=2,constrained_layout=True)

        axs[0][0].plot(time[:1000],signal["samples"][:1000])
        axs[0][0].set_title(signal["label"])
            
        axs[0][1].specgram(signal["samples"],Fs=signal["Fs"])
        axs[0][1].set_title(signal["label"] + " " + "Spectrogram")
        
        axs[1][0].plot(time[:1000],equalized_samples[:1000])
        axs[1][0].set_title("Equalized" + " " + signal["label"])
            
        axs[1][1].specgram(equalized_samples,Fs=signal["Fs"])
        axs[1][1].set_title("Equalized" + " " + signal["label"] + " " + "Spectrogram")
        
        pdf.savefig()
