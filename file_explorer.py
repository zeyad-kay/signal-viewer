from tkinter import filedialog
from helpers import read_edf,save_pdf
import threading

class File_Explorer():
    """
    Show the native file dialog for opening and saving files.
    """
    @staticmethod
    def save_file(root):
        """
        Save a PDF file on another thread.
        """
        filename = filedialog.asksaveasfilename(initialdir = "/",
                                          title = "Save a File",
                                          filetypes = (("PDF files",
                                                        "*.pdf*"),
                                                       ("all files",
                                                        "*.*"))) or None
        if filename is None:
            return None
        
        threading.Thread(target=save_pdf,args=(filename,root.plots_data)).run()

    @staticmethod
    def open_file(root):
        """
        Read data from EDF file and generate a Fileupload event.
        """
        filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("EDF files",
                                                        "*.edf*"),
                                                       ("all files",
                                                        "*.*"))) or None
        
        if filename is None:
            return None
        
        root.new_samples = read_edf(filename)
        root.event_generate("<<Fileupload>>")