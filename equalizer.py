import numpy as np
from helpers import equalize
from slider import Frequency_Slider
import tkinter as tk

class Equalizer_Panel(tk.Frame):
    def __init__(self, master, viewer, Fs, bins=1):
        super().__init__(master)
        self.master = master
        self.Fs = Fs
        self.viewer = viewer
        self.original_fourier = np.fft.fft(viewer.signal["samples"])
        self.equalized_fourier = self.original_fourier
        # main frame
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.frameScale = tk.Frame(self, bd=1, relief="solid")

        self.value = tk.IntVar()
        self.interval_slider = tk.Scale(self.frameScale, orient="horizontal", label="Speed", from_=1,
                                        to=1.9, resolution=0.1, variable=self.value, command=lambda v: self.increase_speed(float(v)))
        self.interval_slider.grid(row=0, column=0, padx=5, pady=3)
        self.value.set(1)
        # creating the sliders loop
        for i in range(bins):
            slider = Frequency_Slider(self.frameScale, fmin=
                (i)*Fs/bins, fmax=(i+1)*Fs/bins)

            slider.grid(row=0, column=i+1)

        self.frameScale.grid(column=0, row=0)

    def increase_speed(self, value):
        for viewer in self.master.viewers:
            viewer.plot(animated=True, interval=2-value)

    def update(self, fmin, fmax, factor):
        self.equalized_fourier = equalize(
            self.original_fourier, self.equalized_fourier, self.viewer.signal["N"],self.viewer.signal["Fs"],fmin, fmax, factor)

        self.viewer.update_equalized_samples(np.fft.ifft(self.equalized_fourier).real)
