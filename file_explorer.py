from tkinter import filedialog

class File_Explorer():
    @staticmethod
    def save_file(root):
        filename = filedialog.asksaveasfilename(initialdir = "/",
                                          title = "Save a File",
                                          filetypes = (("PDF files",
                                                        "*.pdf*"),
                                                       ("all files",
                                                        "*.*"))) or None
        if filename is None:
            return None
        root.event_generate("<<Filesave>>", data=filename)

    @staticmethod
    def browse_file(root):
        filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("EDF files",
                                                        "*.edf*"),
                                                       ("all files",
                                                        "*.*"))) or None
        
        if filename is None:
            return None
        
        root.event_generate("<<Fileupload>>", data=filename)
        