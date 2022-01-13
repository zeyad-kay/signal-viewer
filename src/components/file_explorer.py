from tkinter import filedialog
from core.io import read_edf,save_pdf,read_wav,save_wav
import threading
import re

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
                                          defaultextension="*.pdf",
                                          filetypes = (("PDF files",
                                                        "*.pdf"),
                                                        ("WAV files",
                                                       "*.wav"),
                                                       ("all files",
                                                        "*.*"))) or ""
        if re.search(".wav\Z",filename) is not None:
            threading.Thread(target=save_wav,args=(filename,root.viewer.signal["Fs"],root.viewer.equalized_samples)).run()
        elif re.search(".pdf\Z",filename) is not None:
            threading.Thread(target=save_pdf,args=(filename,root.viewer.signal,root.viewer.time,root.viewer.equalized_samples)).run()
        else:
            return None


    @staticmethod
    def open_file(root):
        """
        Read data from EDF file and generate a Fileupload event.
        """
        filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("EDF files",
                                                        "*.edf*"),
                                                       ("WAV files",
                                                       "*.wav"),
                                                       ("all files",
                                                        "*.*"))) or ""
        
        if re.search(".wav\Z",filename) is not None:
            root.new_signal = read_wav(filename)
            root.event_generate("<<Fileupload>>")
        elif re.search(".edf\Z",filename) is not None:
            root.new_signal = read_edf(filename)
            root.event_generate("<<Fileupload>>")
        else:
            return None