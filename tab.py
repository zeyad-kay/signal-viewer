import tkinter as tk
from toolbar import ToolBar
from viewer import Viewer
from helpers import read_edf
from equalizer import Equalizer_Panel

class Tab(tk.Frame):
    def __init__(self,master=None,samples={}):
        super().__init__(master,background="white")
        self._mode = None
        self.samples = samples
        self.master.add(self,text=self.samples["label"])

        self.create_toolbar()
 
        self.create_viewer(self.samples)
 
        # self.rowconfigure(3,weight=1)
        # toolbar = ToolBar(self)
        # toolbar.grid(row=3,column=0,sticky="nwe")
        # self.rowconfigure(2,weight=1)
        # toolbar = ToolBar(self)
        # toolbar.grid(row=2,column=0,sticky="we")
        self.create_equalizer()

    def create_toolbar(self): 
        self.rowconfigure(0,weight=1)
        toolbar = ToolBar(self)
        toolbar.grid(row=0,column=0,sticky="nwe")

    def delete_tab(self):
        self.master.forget(self.master.select())

    def create_viewer(self,samples):
        self.rowconfigure(1,weight=1)
        self.viewer = Viewer(self,samples,rows=1,columns=1)
        self.viewer.plot(row=0,column=0,animated=True)
        # self.viewer.plot(row=0,column=0,animated=False)
        # self.viewer.plot(row=0,column=1,animated=False)
        # self.viewer.spectrogram(row=1,column=0)
        # self.viewer.spectrogram(row=1,column=1)
        self.viewer.grid(row=1,column=0,sticky="nswe")

    def create_equalizer(self):
        self.rowconfigure(2,weight=1)
        self.equalizer = Equalizer_Panel(self)
        self.equalizer.grid(row=2,column=0,sticky="")

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
