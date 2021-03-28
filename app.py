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

    def read_data(self):
        self.plots_data.append(read_file("sampleECG.edf"))

    def create_viewer(self,data):
        viewer = Viewer(self.master,self.viewers.__len__(),data)
        return viewer

    def create_widgets(self):
        self.create_menubar()
        self.create_toolbar()
        
        def delete_viewers():
            for viewer in self.viewers:
                viewer.cleanup()
            self.viewers = []
        
        def plot_signal(e):
            self.read_data()
            delete_viewers()

            for i,plot in enumerate(self.plots_data):
                self.master.rowconfigure(i+1,weight=1)
                v=self.create_viewer(plot)
                v.grid(row=i+1,columns=1,sticky = 'nswe')
                self.viewers.append(v)
                v.add_plot()
        
        self.master.bind("<KeyPress>",plot_signal)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(background='white')
    app = Application(master=root)
    app.mainloop()