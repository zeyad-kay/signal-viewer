import tkinter as tk
import sys
from .file_explorer import File_Explorer 

class MenuBar(tk.Menu):
    def __init__(self, master):
        super().__init__(master)

        fileMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Open File",  command=lambda : File_Explorer.open_file(master))
        fileMenu.add_separator() 
        fileMenu.add_command(label="Exit",  command=self.quit)

    def quit(self):
        sys.exit(0)