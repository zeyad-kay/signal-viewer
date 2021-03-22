import tkinter as tk
from tkinter import filedialog
from helpers import read_file

class File_Explorer(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.button = tk.Button(self,text = "Browse Files",command=self.browse_files)
        self.button.pack(side="top")
        self.content = None

    def browse_files(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))        
        if filename is not None:
            self.content = read_file(filename)
            self.master.event_generate("<<Fileread>>")
            # print(self.content)