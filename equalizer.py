import numpy as np
from helpers import equalize
from slider import Frequency_Slider
import tkinter as tk

class Equalizer_Panel(tk.Frame):
    def __init__(self, master, viewer, Fs, bins=1):
        super().__init__(master,bd=1, relief="solid")
        self.master = master
        self.bins = bins
        self.Fs = Fs
        self.viewer = viewer
        self.original_fourier = np.fft.fft(viewer.signal["samples"])
        self.equalized_fourier = self.original_fourier
        # main frame
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.frameScale = tk.Frame(self)
        self.intervalScale = tk.Frame(self)

        self.interval_value = tk.IntVar()
        self.interval_slider = tk.Scale(self.intervalScale, orient="horizontal", label="Speed", from_=1,
                                        to=1.9, resolution=0.1, variable=self.interval_value, command=lambda v: self.increase_speed(float(v)))
        self.interval_slider.grid(row=0, column=0, padx=5, pady=3)
        self.interval_value.set(1)
        
        self.fmin_value = tk.IntVar()
        self.fmin_slider = tk.Scale(self.intervalScale, orient="horizontal", label="Fmin (Hz)", from_=1,
                                        to=self.Fs/2, resolution=1, variable=self.fmin_value)
        self.fmin_slider.grid(row=1, column=0, padx=5, pady=3)
        self.fmin_value.set(1)
        
        self.fmax_value = tk.IntVar()
        self.fmax_slider = tk.Scale(self.intervalScale, orient="horizontal", label="Fmax (Hz)", from_=1,
                                        to=self.Fs/2, resolution=1, variable=self.fmax_value)
        self.fmax_slider.grid(row=2, column=0, padx=5, pady=3)
        self.fmax_value.set(self.Fs/2)

        self.update_range_btn = tk.Button(self.intervalScale,command=lambda : self.update_range(),text="Update Range")
        self.update_range_btn.grid(row=3,column=0, padx=5, pady=3)
        # creating the sliders loop
        for i in range(bins):
            slider = Frequency_Slider(self.frameScale, fmin=
                (i)*(Fs/2)/bins, fmax=(i+1)*(Fs/2)/bins)

            slider.grid(row=0, column=i+1)

        self.intervalScale.grid(column=0, row=0)
        self.frameScale.grid(column=1, row=0)

    def increase_speed(self, value):
        self.viewer.plot(animated=True, interval=2-value)

    def update_spectrogram(self, fmin, fmax, inclusive_factor,exclusive_factor=1):
        
        self.equalized_fourier = equalize(
            self.original_fourier, self.equalized_fourier, self.viewer.signal["N"],self.viewer.signal["Fs"],fmin, fmax, inclusive_factor,exclusive_factor)
        
        self.viewer.update_equalized_samples(np.fft.ifft(self.equalized_fourier).real)
        
        self.viewer._figure.axes[1].set_ylim(self.fmin_value.get(),self.fmax_value.get())
        self.viewer._figure.axes[3].set_ylim(self.fmin_value.get(),self.fmax_value.get())
        self.viewer._figure.canvas.draw_idle()

    def update_range(self):
        fmin = self.fmin_value.get()
        fmax = self.fmax_value.get()
        diff = fmax - fmin

        for i,slider in enumerate(self.frameScale.children.values()):
            slider.set_range(fmin + (i)*diff/self.bins,fmin + (i+1)*diff/self.bins)
        
        self.update_spectrogram(fmin,fmax,1,0)