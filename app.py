import tkinter as tk
from toolbar import ToolBar
from menu import MenuBar
from viewer import Viewer

class Application(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self._mode = None
        self.viewers = []
        self.plots_data = []
        self.create_widgets()

    def create_widgets(self):
        """
        Create all initial components and listen for Fileupload event.
        """
        self.create_menubar()
        self.create_toolbar()

        # Start listening for file upload event
        # to start plotting the signals
        self.master.bind("<<Fileupload>>",self.plot_signals)
        
    def create_menubar(self):
        self.master.config(menu=MenuBar(self))

    def create_toolbar(self):        
        self.grid(row=0,sticky='w')
        self.toolbar = ToolBar(self)
    
    def create_viewer(self,data):
        v = Viewer(self.master,self.viewers.__len__(),data)
        
        self.master.rowconfigure(self.viewers.__len__()+1,weight=1)
        v.grid(row=self.viewers.__len__()+1,columns=1,sticky = 'nswe')
        
        v.draw(animate=True,interval=0.1,spectrogram=True)
        self.viewers.append(v)
            
    def clear_plots(self):
        """
        Reset the screen by deleting all plots.
        """
        # Stops animation before deleting the plot
        # Needs some smoothing up!!
        for viewer in self.viewers:
            viewer.cleanup()
        
        self.viewers = []
    
    def plot_signals(self,e):
        """
        Iterate over loaded data and draw the plots
        """
        self.clear_plots()
        
        for i,plot in enumerate(self.plots_data):
            self.create_viewer(plot)

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

if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')
    root.title("Signal Viewer")
    root.configure(background='white')
    app = Application(master=root)
    app.mainloop()