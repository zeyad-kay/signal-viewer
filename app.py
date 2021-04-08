from helpers import read_edf
import tkinter as tk
from tkinter import ttk
from tab import Tab
from menu import MenuBar

class Application(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        # Just for testing
        self.plots_data = []
        self.create_widgets()

    def create_widgets(self):
        """
        Create all initial components and listen for Fileupload event.
        """
        self.master.grid_columnconfigure(0,weight=1)
        self.master.grid_rowconfigure(0,weight=1)
        self.grid(sticky="nsew")

        self.master.config(menu=MenuBar(self))

        # Tabs container
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.tabs_container = ttk.Notebook(self)
        self.tabs_container.grid(row=0,column=0,sticky="nsew")
        
        # Start listening for file upload event
        # to create a new tab
        self.master.bind("<<Fileupload>>",lambda e: self.create_tab())
    
    def create_tab(self,name="Untitled"):
        tab = Tab(self.tabs_container,name)
        tab.columnconfigure(0,weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')
    root.title("Signal Viewer")
    app = Application(master=root)
    app.mainloop()