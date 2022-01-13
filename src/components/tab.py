import tkinter as tk
from .toolbar import ToolBar
from .viewer import Viewer
from .equalizer import Equalizer_Panel

class Tab(tk.Frame):
    def __init__(self,master=None,signal={}):
        super().__init__(master,background="white")
        self._mode = None

        self.signal = signal
        self.master.add(self,text=self.signal["label"])

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.rowconfigure(3,weight=1)
        
        self.create_viewer(self.signal)
        self.viewer.grid(row=1,column=0,sticky="nswe")
        
        self.create_toolbar(self.viewer)
        self.toolbar.grid(row=0,column=0,sticky="nwe")
        
        self.create_equalizer(self.viewer,self.signal["Fs"],bins=10)
        self.equalizer.grid(row=2,column=0,sticky="")

    def create_toolbar(self,viewer):
        self.toolbar = ToolBar(self,viewer)

    def delete_tab(self):
        self.master.forget(self.master.select())

    def create_viewer(self,signal):
        self.viewer = Viewer(self,signal,rows=2,columns=2)
        self.viewer.plot(animated=True,interval=1)
        self.viewer.spectrogram()

    def create_equalizer(self, viewer,Fs, bins):
        self.equalizer = Equalizer_Panel(self, viewer, Fs, bins)

    def set_mode(self,mode):
        # Reset mode if it is already selected
        if self._mode == mode: 
            self._mode = None
        else:
            self._mode = mode
        self.set_cursor(self._mode)
    
    def get_mode(self):
        return self._mode
    
    def set_cursor(self,mode):
        cursor_mode_mapping = {
            "zoomIn":"plus",
            "zoomOut":"circle",
            "pan":"fleur"
        }
        if mode is None:
            cursor = "arrow"
        else:
            cursor = cursor_mode_mapping[mode]
        self.master.config(cursor=cursor)
