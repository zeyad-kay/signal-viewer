import tkinter as tk
from matplotlib.pyplot import rcParams
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

class Viewer(tk.Frame):
    def __init__(self,master=None,order=0,data={}):
        super().__init__(master)
        self.master = master
        self.order = order
        self.zoom_scale = 2
        self._play = True
        self.data = data

    def __render_plot(self):
        
        self._figure.subplots(1,1)
        line = self._figure.axes[0].plot([],[])[0]
        
        def init():
            line.axes.legend([self.data["label"]])
            line.axes.set_xlim(0,self.data["x"][1000])
            line.axes.set_ylim(min(self.data["y"]) * self.zoom_scale,max(self.data["y"]) * self.zoom_scale)
            line.axes.set_xlabel("Time")
            line.axes.set_ylabel("Amplitude")
            line.axes.grid(True)
            return [line]
        
        def update(frame):
            try:
                x = self.data["x"][:frame + 1]
                y = self.data["y"][:frame + 1]
                
                # adjust scale
                xmin,xmax = self._figure.axes[0].get_xlim()
                ymin,ymax = self._figure.axes[0].get_ylim()
                scaled = False
                if x[-1] > xmax:
                    self._figure.axes[0].set_xlim(xmin,x[-1] * self.zoom_scale)
                    scaled = True
                if y[-1] > ymax:
                    self._figure.axes[0].set_ylim(ymin,y[-1] * self.zoom_scale)
                    scaled = True
                if y[-1] < ymin:
                    self._figure.axes[0].set_ylim(y[-1] * self.zoom_scale , ymax)
                    scaled = True
                if scaled:
                    # Should be called whenever the figure changes 
                    self._figure.canvas.draw_idle()
                
                # Always flush to give control back to the GUI event loop
                # and not freeze the app
                self._figure.canvas.flush_events()
                line.set_data(x, y)
                return [line]
            except Exception as e:
                print(e)
     
        
        # Setting the Interval too low messes up the the event loop
        # when there are multiple plots
        self._animation = FuncAnimation(self._figure, update,
            init_func=init, interval=100,blit=True,repeat=False)
        
        # Initial draw
        self._figure.canvas.draw_idle()
        self._figure.canvas.get_tk_widget().grid(row=self.order+1,columns=1,sticky = 'nswe')        

    def add_plot(self):
        # inches to pixel conversion    
        px = 1/rcParams['figure.dpi']
        self._figure = Figure(figsize=((self.master.winfo_screenwidth())*px, (self.master.winfo_screenheight())*px),constrained_layout=True)
        FigureCanvasTkAgg(self._figure, master=self.master)
        
        self.__render_plot()
        self.__register_event_listeners()
        
    def __register_event_listeners(self):
        self.__add_play_listener()
        self.__add_cursor_listener()
    
    def __add_cursor_listener(self):
        self._figure.canvas.mpl_connect('button_press_event', self.__cursor_control)
    
    def __add_play_listener(self):
        def toggle():
            if self._play :
                self.pause()
                self._play_pause_icon = tk.PhotoImage(file="images/play.png")
            else:
                self.play()
                self._play_pause_icon = tk.PhotoImage(file="images/pause.png")
            self._play_btn["image"] = self._play_pause_icon
        
        self._play_pause_icon = tk.PhotoImage(file="images/pause.png")
        self._play_btn = tk.Button(self.master,bd=0,bg="white")
        self._play_btn["image"]=self._play_pause_icon
        self._play_btn.configure(command=lambda : toggle())
        self._play_btn.grid(row=self.order+1,columns=1)
    
    def __cursor_control(self,event):

        cursor_control_mapping = {
            "plus":self.zoom_in,
            "circle":self.zoom_out,
            "fleur":self.pan
        }
        cursor = self.master.children["!application"].get_cursor()
        
        if cursor_control_mapping.get(cursor) is not None:
            cursor_control_mapping[cursor](event)
        
        # self._figure.canvas.draw_idle()
        # self._figure.canvas.flush_events()
    
    def pan(self,original_event):
                
        def release(new_event):
            self._figure.canvas.mpl_disconnect(self.drag_listener)
            self._figure.canvas.mpl_disconnect(self.release_listener)
        
        def drag(new_event):
            # In case of scrolling outside the axis
            x = new_event.xdata or original_event.xdata
            y = new_event.ydata or original_event.ydata
            
            xmin,xmax = self._figure.axes[0].get_xlim()
            ymin,ymax = self._figure.axes[0].get_ylim()
            
            dx = original_event.xdata - x
            dy = original_event.ydata - y

            self._figure.axes[0].set_xlim(xmin + dx,xmax + dx)
            self._figure.axes[0].set_ylim(ymin + dy,ymax + dy)
            self._figure.canvas.draw_idle()
            # self._figure.canvas.flush_events()    

        self.drag_listener = self._figure.canvas.mpl_connect("motion_notify_event", drag)
        self.release_listener = self._figure.canvas.mpl_connect("button_release_event", release)


    def zoom_out(self,event):
        ymin,ymax = self._figure.axes[0].get_ylim()
        xmin,xmax = self._figure.axes[0].get_xlim()
        
        self._figure.axes[0].set_xlim(xmin * self.zoom_scale, xmax * self.zoom_scale)
        self._figure.axes[0].set_ylim(ymin * self.zoom_scale, ymax * self.zoom_scale)
        
        self._figure.canvas.draw_idle()
        self._figure.canvas.flush_events()
        print(self._figure.stale)

    def zoom_in(self,event):
        xmin,xmax = self._figure.axes[0].get_xlim()
        ymin,ymax = self._figure.axes[0].get_ylim()
        
        self._figure.axes[0].set_xlim(xmin / self.zoom_scale, xmax / self.zoom_scale)
        self._figure.axes[0].set_ylim(ymin / self.zoom_scale, ymax / self.zoom_scale)
        self._figure.canvas.draw_idle()
        self._figure.canvas.flush_events()
        print(self._figure.stale)

    def pause(self):
        self._animation.event_source.stop()
        self._play = False
        self._figure.canvas.flush_events()
    
    def play(self):
        self._animation.event_source.start()
        self._play = True
        self._figure.canvas.flush_events()
    
    def cleanup(self):    
        self.pause()
        self.destroy()