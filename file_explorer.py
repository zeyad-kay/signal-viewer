from tkinter import filedialog

class File_Explorer():
    """
    Show the native file dialog for opening and saving files.
    """
    @staticmethod
    def save_file(root):
        """
        Generate a Filesave event when the user chooses to save a file
        """
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
    def open_file(root):
        """
        Generate a Fileupload event when the user chooses to open a file
        """
        filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("EDF files",
                                                        "*.edf*"),
                                                       ("all files",
                                                        "*.*"))) or None
        
        if filename is None:
            return None
        
        root.event_generate("<<Fileupload>>", data=filename)