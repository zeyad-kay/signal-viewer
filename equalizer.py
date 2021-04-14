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
            slider = Frequency_Slider(self.frameScale, fmin=int(
                (i)*Fs/bins + 1), fmax=int((i+1)*Fs/bins))

            slider.grid(row=0, column=i+1)

        self.frameScale.grid(column=0, row=0)

    def increase_speed(self, value):
        for viewer in self.master.viewers:
            viewer.plot(animated=True, interval=2-value)

    def update(self, fmin, fmax, factor):
        equalized_samples = equalize(
            self.original_fourier, np.fft.fft(self.viewer.equalized_samples), fmin, fmax, factor)

        self.viewer.update_equalized_samples(equalized_samples)
