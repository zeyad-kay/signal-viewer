import tkinter as tk
from file_explorer import File_Explorer

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()


    def create_widgets(self):
        self.explorer = File_Explorer(self)
        # sets the position
        self.explorer.pack(side="top")

        self.label = tk.Label(self)
        
        def set_label(e):
            self.label["text"]=self.explorer.content

        self.bind("<<Fileread>>", set_label)   
        self.label.pack()
        
root = tk.Tk()
app = Application(master=root)
app.mainloop()