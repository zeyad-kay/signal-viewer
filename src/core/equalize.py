import numpy as np

def equalize(original_fourier,current_equalized_fourier,N,Fs,fmin,fmax,inclusive_factor=1,exclusive_factor=1):
    # boundary condition for the last slider
    if Fs/2 == fmax:
        fmax = fmax + 1
    
    freq = np.fft.fftfreq(N,1/Fs)
    equalized_fourier = []
    for i,freq in enumerate(freq):
        if abs(freq) >= fmin and abs(freq) < fmax:
            equalized_fourier.append(original_fourier[i]*inclusive_factor)   
        else:
            equalized_fourier.append(current_equalized_fourier[i]*exclusive_factor)

    equalized_fourier = np.array(equalized_fourier)
    return equalized_fourier
