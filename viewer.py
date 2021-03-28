import tkinter as tk
from matplotlib.pyplot import rcParams
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

class Viewer(tk.Frame):
    def __init__(self,master=None,index=0,data={}):
        super().__init__(master)
        self.master = master
        self.index = index
        self._plot = None
        self.play = True
        self.data = data

    def __render_plot(self):
        
        self._figure.subplots(1,1)
        line = self._figure.axes[0].plot([],[])[0]
        def init():
            line.axes.set_xlim(0,10)
            line.axes.set_ylim(-10,10)
            # line.axes.autoscale()
            line.axes.set_xlabel("Time")
            line.axes.set_ylabel("Amplitude")
            line.axes.grid(True)
            return [line]
        
        def update(frame):
            try:
                x = self._plot["x"][:frame + 1]
                y = self._plot["y"][:frame + 1]
                xmin,xmax = line.axes.get_xlim()
                ymin,ymax = line.axes.get_ylim()
                if x[-1] > xmax:
                    line.axes.set_xlim(xmin,xmax*2)
                if y[-1] > ymax:    
                    line.axes.set_ylim(ymin,ymax*2)
                line.set_data(x, y)
                return [line]
            except Exception as e:
                print("---------Err---------")
                # print(x)
     
        def toggle():
            if self.play :
                self.__pause()
                self._play_btn["text"] = "play"
            else:
                self.__play()
                self._play_btn["text"] = "pause"


        
        self._animation = FuncAnimation(self._figure, update,
            init_func=init, interval=1,blit=True,repeat=False)
        
        self._play_btn = tk.Button(self.master,text="pause")
        self._play_btn.configure(command=lambda : toggle())
        self._play_btn.grid(row=self.index+1,columns=1)
        
        self._figure.canvas.draw_idle()
        self._figure.canvas.get_tk_widget().grid(row=self.index+1,columns=1,sticky = 'nswe')
        self._figure.canvas.mpl_connect('axes_enter_event', self.control)    
    
    def add_plot(self):
                
        px = 1/rcParams['figure.dpi']
        
        self._plot = dict({
            "play":False,
            "x": self.data["x"],
            "y": self.data["y"],
            "label": self.data["label"]
        })

        self._figure = Figure(figsize=((self.master.winfo_screenwidth())*px, (self.master.winfo_screenheight())*px),constrained_layout=True)
        FigureCanvasTkAgg(self._figure, master=self.master)
        
        self.__render_plot()
        

        # pack_toolbar=False will make it easier to use a layout manager later on.
        
    def __pause(self):
        self._animation.event_source.stop()
        self.play = False
    def __play(self):
        self._animation.event_source.start()
        self.play = True
    
    def control(self,e):
        control_mapping = {
            "plus":self.zoom_in,
            "circle":self.zoom_out,
            "fleur":self.pan
        }
        control_mapping[self.master.get_cursor()]()
        # self._figure.axes[0].set_xticks(range(0,3))
        # self._figure.axes[0].set_xticklabels(range(0,3))
        # self._figure.axes[0].set_xticks(range(0,20))
        # self._figure.axes[0].set_yticklabels(range(0,20))
        # self._figure.axes[0].start_pan(e.xdata,e.ydata,3)
        # self.master.change_cursor(self.master.get_cursor())

    def pan(self):
        print("pan")
    
    def zoom_in(self):
        print("in")

    def zoom_out(self):
        print("out")
    
    def cleanup(self):    
        self.__pause()
        self.destroy()