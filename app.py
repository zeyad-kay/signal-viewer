from helpers import read_file
import tkinter as tk
from toolbar import ToolBar
from menu import MenuBar
from viewer import Viewer

class Application(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.pointer = "arrow"
        self.viewers = []
        self.plots_data = []
        self.create_widgets()

    def create_menubar(self):
        self.master.config(menu=MenuBar(self))

    def create_toolbar(self):        
        self.grid(row=0)
        self.toolbar = ToolBar(self)

    def get_cursor(self):
        return self.pointer
    
    def change_cursor(self,ctype):
        if self.pointer != ctype:
            self.pointer=ctype
        else:
            self.pointer = "arrow"
        self.master.config(cursor=self.pointer)

    def create_viewer(self,data):
        viewer = Viewer(self.master,self.viewers.__len__(),data)
        return viewer
    
    def delete_viewers(self):
        for viewer in self.viewers:
            # Stops animation before deleting the plot
            # Needs some smoothing up!!
            viewer.cleanup()
        self.viewers = []

    def create_widgets(self):
        self.create_menubar()
        self.create_toolbar()
        
        def plot_signal(filename):
            self.plots_data.append(read_file(filename))
            self.delete_viewers()
            
            for i,plot in enumerate(self.plots_data):
                self.master.rowconfigure(i+1,weight=1)
                v=self.create_viewer(plot)
                v.grid(row=i+1,columns=1,sticky = 'nswe')
                self.viewers.append(v)
                v.add_plot()
        
        # Only way to pass data across events
        callback = self.master.register(plot_signal)
        self.master.call("bind", self.master, "<<Fileupload>>", callback + " %d")
        
        # Testing
        self.master.event_generate("<KeyPress>")
        self.master.bind("<KeyPress>",lambda e: self.master.event_generate("<<Fileupload>>",data="SampleECG.edf"))

if __name__ == "__main__":
    root = tk.Tk()
    width = root.winfo_screenwidth() 
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))
    root.title("Signal Viewer")
    root.configure(background='white')
    app = Application(master=root)
    app.mainloop()