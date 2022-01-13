import tkinter as tk

class Frequency_Slider(tk.Frame):
    def __init__(self, master, fmin, fmax):
        super().__init__(master)
        self.master = master
        self.fmin = fmin
        self.fmax = fmax
        self.label = tk.Label(self, text=f"{int(fmax)} Hz")
        self.label.grid(row=0, column=0)

        self.value = tk.IntVar()
        self.scale = tk.Scale(self, from_=5, variable=self.value, resolution=1, to=0, command=lambda factor: master.master.update_spectrogram(self.fmin,self.fmax,int(factor)))
        self.scale.grid(row=1, column=0)
        self.value.set(1)
    
    def set_range(self,fmin,fmax):
        self.fmin = fmin
        self.fmax = fmax
        self.label["text"] = f"{int(fmax)} Hz"
        self.value.set(1)