from helpers import read_edf,save_pdf
import tkinter as tk
from toolbar import ToolBar
from menu import MenuBar
from viewer import Viewer
import threading

class Application(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.pointer = "arrow"
        self.viewers = []
        self.plots_data = []
        self.create_widgets()

    def create_menubar(self):
        self.master.config(menu=MenuBar(self))

    def create_toolbar(self):        
        self.grid(row=0,sticky='w')
        self.toolbar = ToolBar(self)

    def get_cursor(self):
        return self.pointer
    
    def set_cursor(self,ctype):
        if self.pointer != ctype:
            self.pointer = ctype
        else:
            self.pointer = "arrow"
        self.master.config(cursor=self.pointer)

    def create_viewer(self,data):
        viewer = Viewer(self.master,self.viewers.__len__(),data)
        return viewer
    
    def delete_viewers(self):
        for viewer in self.viewers:
            # Stops animation before deleting the plot
            # Needs some smoothing up!!
            viewer.cleanup()
        self.viewers = []

    def create_widgets(self):
        self.create_menubar()
        self.create_toolbar()

        # Only way to pass data across events
        upload_callback = self.master.register(self.plot_signal)
        self.master.call("bind", self.master, "<<Fileupload>>", upload_callback + " %d")
        
        save_callback = self.master.register(self.save_signals)
        self.master.call("bind", self.master, "<<Filesave>>", save_callback + " %d")

    def plot_signal(self,filename):
        self.plots_data.append(read_edf(filename))
        self.delete_viewers()
        
        for i,plot in enumerate(self.plots_data):
            self.master.rowconfigure(i+1,weight=1)
            v=self.create_viewer(plot)
            v.grid(row=i+1,columns=1,sticky = 'nswe')
            self.viewers.append(v)
            v.add_plot()
        
    def save_signals(self,filename):
        if self.viewers.__len__():    
            try:
                t = threading.Thread(target=save_pdf,args=(filename,self.plots_data))
                t.run()
            except Exception as e:
                print(e)

if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed')
    root.title("Signal Viewer")
    root.configure(background='white')
    app = Application(master=root)
    app.mainloop()