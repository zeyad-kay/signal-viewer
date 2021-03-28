import tkinter as tk
from tkinter.constants import TOP, X
from toolbar import ToolBar
from menu import MenuBar
from viewer import Viewer

import numpy as np
i = 1

def dummy(c):
    global i
    i = i+1
    # print(i)
    x = np.arange(0, 3, .01)
    if(i % 2 == 0):
        y = np.sin(c * np.pi * x)
    else:
        y = np.cos(c * np.pi * x)
    return {"i": i, "x": x, "y": y, "label": str(i)}


class Application(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)

        self.master = master
        # self.grid(column=1)
        self.pointer = "arrow"
        self.viewers = []
        self.plots_data = []
        self.create_widgets()

    def create_menubar(self):
        self.master.config(menu=MenuBar(self))

    def create_toolbar(self):        
        self.grid(row=0)
        self.toolbar = ToolBar(self)
        # self.toolbar.columnconfigure(2,weight=1)
        # self.toolbar.columnconfigure(3,weight=1)
        # self.toolbar.columnconfigure(4,weight=1)

    def get_cursor(self):
        return self.pointer
    
    def change_cursor(self,ctype):
        if self.pointer != ctype:
            self.pointer=ctype
        else:
            self.pointer = "arrow"
        self.master.config(cursor=self.pointer)

    def read_data(self):
        self.plots_data.append(dummy(1))

    def create_viewer(self,data):
        viewer = Viewer(self.master,self.viewers.__len__(),data)
        return viewer

    def create_widgets(self):
        self.create_menubar()
        # self.toolbar = ToolBar(self)
        # self.toolbar2 = ToolBar(self)
        self.create_toolbar()
        # self.create_toolbar()
        
        def delete_viewers():
            for viewer in self.viewers:
                viewer.cleanup()
            self.viewers = []
        
        def plot_signal(e):
            self.read_data()
            delete_viewers()
            for i,plot in enumerate(self.plots_data):
                # self.master.rowconfigure(i+1,weight=1)
                self.master.rowconfigure(i+1,weight=1)
                v=self.create_viewer(plot)
                v.grid(row=i+1,columns=1,sticky = 'nswe')
                self.viewers.append(v)
                v.add_plot()
        
        self.master.bind("<KeyPress>",plot_signal)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(background='white')
    # root.columnconfigure(0,weight=1)
    app = Application(master=root)
    app.mainloop()