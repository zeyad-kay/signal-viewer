import tkinter as tk
from tkinter import ttk
from components import Tab, MenuBar

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.new_signal = {}
        self.create_widgets()

    def create_widgets(self):
        """
        Create all initial components and listen for Fileupload event.
        """
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.grid(sticky="nsew")

        self.master.config(menu=MenuBar(self))

        # Tabs container
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.tabs_container = ttk.Notebook(self)
        self.tabs_container.grid(row=0, column=0, sticky="nsew")

        # Start listening for file upload event
        # to create a new tab
        self.master.bind("<<Fileupload>>",
                         lambda e: self.create_tab(self.new_signal))

    def create_tab(self, signal):
        # for tab in self.tabs_container.children.values():
        #     tab.toolbar.toggle_play()
        tab = Tab(self.tabs_container, signal)
        tab.columnconfigure(0, weight=1)
        self.tabs_container.select(tab)

if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')
    root.title("Signal Viewer")
    app = Application(master=root)
    app.mainloop()
