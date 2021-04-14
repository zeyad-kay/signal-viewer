import tkinter as tk
from toolbar import ToolBar
from viewer import Viewer
from equalizer import Equalizer_Panel

class Tab(tk.Frame):
    def __init__(self,master=None,samples={}):
        super().__init__(master,background="white")
        self._mode = None
        self.viewers = []
        # self.samples = samples
        from audio import signal ############### testing
        self.signal = signal ############### testing
        # self.equalized_samples = signal
        self.master.add(self,text=self.signal["label"])

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.rowconfigure(3,weight=1)
        
        self.create_toolbar().grid(row=0,column=0,sticky="nwe")
        
        self.create_viewer(self.signal).grid(row=1,column=0,sticky="nswe")

        self.create_viewer(self.signal).grid(row=2,column=0,sticky="nswe")

        self.create_equalizer(self.signal,10)
        self.equalizer.grid(row=3,column=0,sticky="")

        # for slider in self.equalizer.sliders:
        #     print(slider['variable'])
            # slider["command"] = lambda e: print(f"slider {slider['variable']} : {e}")

    def create_toolbar(self):
        return ToolBar(self)

    def delete_tab(self):
        self.master.forget(self.master.select())

    def create_viewer(self,signal):
        viewer = Viewer(self,signal,rows=1,columns=2)
        viewer.plot(animated=True,interval=1)
        viewer.spectrogram()
        self.viewers.append(viewer)
        return viewer
    
    def create_equalizer(self, samples, bins):
        self.equalizer = Equalizer_Panel(self, samples, bins)

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
