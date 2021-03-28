import tkinter as tk
from matplotlib.pyplot import rcParams
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

class Viewer(tk.Frame):
    def __init__(self,master=None,index=0,data={}):
        super().__init__(master)
        self.master = master
        self.index = index
        self._plot = None
        self.play = True
        self.data = data
        self.scale = 1

    def __render_plot(self):
        
        self._figure.subplots(1,1)
        line = self._figure.axes[0].plot([],[])[0]
        def init():
            line.axes.set_xlim(0,self.data["x"][100])
            # line.axes.set_xlim(0,self.data["x"][-1])
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
     
        def toggle():
            if self.play :
                self.__pause()
                self._play_btn["text"] = "play"
            else:
                self.__play()
                self._play_btn["text"] = "pause"


        
        self._animation = FuncAnimation(self._figure, update,
            init_func=init, interval=0.001,blit=True,repeat=False)
        
        self._play_btn = tk.Button(self.master,text="pause")
        self._play_btn.configure(command=lambda : toggle())
        self._play_btn.grid(row=self.index+1,columns=1)
        
        self._figure.canvas.draw_idle()
        self._figure.canvas.get_tk_widget().grid(row=self.index+1,columns=1,sticky = 'nswe')

        def control(e):
            
            # self._figure.canvas.mpl_disconnect
            def pan():
                self._figure.axes[0].start_pan(1,e.xdata,e.ydata)
                
                def drag(ev):
                    self._figure.axes[0].drag_pan(1,None,ev.xdata,ev.ydata)
                    print(self._figure.axes[0].get_lines())

                # self._figure.canvas.mpl_connect('button_release_event', drag)

            def zoom_out():
                # self._figure.axes[0].set_xlim(0,20)
                # line.axes.set_xlim(0,30)
                # line.axes.set_xticklabels(range(0,20))
                # line.axes.set_xticks(range(0,20))
                # line.axes.set_xticks(range(0,30,10))
                # line.axes.set_xticklabels(range(0,30,10))
                xmin,xmax = line.axes.get_xlim()
                ymin,ymax = line.axes.get_ylim()
                if self.scale > 1 :
                    self.scale = self.scale - 1
                line.axes.set_xlim(self.scale * xmin,self.scale * xmax)
                line.axes.set_ylim(self.scale * ymin,self.scale * ymax)
            def zoom_in(x,y):
                xmin,xmax = line.axes.get_xlim()
                ymin,ymax = line.axes.get_ylim()
                self.scale = self.scale + 1    
                line.axes.set_xlim(xmin / self.scale , xmax / self.scale)
                line.axes.set_ylim(ymin / self.scale, ymax / self.scale)
                # self._figure.axes[0].callbacks.connect('xlim_changed', lambda event: self._animation._blit_cache.clear())
                # self._figure.axes[0].callbacks.connect('ylim_changed', lambda event: self._animation._blit_cache.clear())
            
            control_mapping = {
                "plus":zoom_in,
                "circle":zoom_out,
                "fleur":pan
            }
            
            app = self.master.children["!application"]
            if app.get_cursor() == "arrow":
                print("arr")
            else:
                control_mapping[app.get_cursor()]()
            
            self._figure.canvas.draw_idle()
        
        self.cid = self._figure.canvas.mpl_connect('button_press_event', control)
        
        

    
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
        app = self.master.children["!application"]
        if app.get_cursor() == "arrow":
            print("arr")
        else:
            control_mapping[app.get_cursor()]()
            
        # self._figure.axes[0].set_xticks(range(0,3))
        # self._figure.axes[0].set_xticklabels(range(0,3))
        # self._figure.axes[0].set_xticks(range(0,20))
        # self._figure.axes[0].set_yticklabels(range(0,20))
        # self._figure.axes[0].start_pan(e.xdata,e.ydata,3)
        # self.master.change_cursor(self.master.get_cursor())

    # def pan(self):
    #     print("pan")
    
    # def zoom_in(self):
    #     print("oo")
    #     # self._figure.axes[0].set_xlim(0,20)
    #     line.axes.set_xticks(range(0,20))
    #     line.axes.set_xticklabels(range(0,20))

    # def zoom_out(self):
    #     print("out")
    
    def cleanup(self):    
        self.__pause()
        self.destroy()