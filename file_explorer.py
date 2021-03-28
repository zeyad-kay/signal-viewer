from tkinter import filedialog
from helpers import read_file

class File_Explorer():
    
    @staticmethod
    def browse_files():
        filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*"))) or None
        
        if filename is None:
            return None
        
        return read_file(filename)

    def read_file(filename):
        return {}