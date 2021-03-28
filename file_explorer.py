from tkinter import filedialog
from helpers import read_file

class File_Explorer():
    
    @staticmethod
    def browse_files(root):
        filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("EDF files",
                                                        "*.edf*"),
                                                       ("all files",
                                                        "*.*"))) or None
        
        if filename is None:
            return None
        
        root.event_generate("<<Fileupload>>", data=filename)
        