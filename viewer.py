import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import numpy as np

class Viewer(tk.Frame):
    """
    Visual component for viewing data on a Matplotlib Figure.
    """

    def __init__(self, master=None, signal={}, rows=1, columns=1):
        super().__init__(master, background="white")
        self.master = master
        self.zoom_scale = 1.1
        self.playing = True
        self.points_per_draw = 30
        self.signal = signal
        self.equalized_samples = signal["samples"].copy()
        self.time = np.linspace(0, self.signal["N"] * 1/self.signal["Fs"], self.signal["N"])
        self.current_frame = 1
        self._animation = None
        self.modes = {
            "zoomIn": self.zoom_in,
            "zoomOut": self.zoom_out,
            "pan": self.pan
        }

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.__create_figure(rows, columns)

    def __create_figure(self, rows, columns):
        """
        Create a matplotlib Figure and initialize the grid.
        """

        self._figure = Figure(figsize=(2, 2), constrained_layout=True)
        FigureCanvasTkAgg(self._figure, master=self)
        self._figure.subplots(rows, columns)
        self._figure.canvas.get_tk_widget().grid(row=0, column=0, sticky='nswe')

        self._figure.canvas.mpl_connect('axes_enter_event', self.__mode_listener)
        self._figure.canvas.mpl_connect(
            'axes_leave_event', lambda e: self._figure.canvas.mpl_disconnect(self.button_listener))
        self.draw_listener = self._figure.canvas.mpl_connect(
            'draw_event', self.__check_end_of_animation)

    def __mode_listener(self, e):
        self.button_listener = self._figure.canvas.mpl_connect(
            'button_press_event', self.__mode_control)
    
    def __check_end_of_animation(self,event):
        if self.current_frame * self.points_per_draw > self.signal["N"]:
            print(self.current_frame)
            self.pause()
    
    def update_equalized_samples(self, new_samples):
        self.equalized_samples = new_samples
        self._figure.axes[0].set_ylim(
                min(self.equalized_samples), max(self.equalized_samples))
        self._figure.axes[0].get_lines()[0].set_data(self.time[:(self.current_frame-1) * self.points_per_draw],self.equalized_samples[:(self.current_frame-1) * self.points_per_draw])
        cmap = self.master.toolbar.selected_color.get()
        self.spectrogram(self.equalized_samples,self.signal["Fs"],cmap)

    def spectrogram(self, samples, Fs,cmap="spring"):
        try:
            self._figure.axes[1].clear()
            self._figure.axes[1].specgram(samples, Fs=Fs,cmap=cmap)
            self._figure.canvas.draw_idle()
            self._figure.canvas.flush_events()
        except Exception as e:
            print(e)

    def plot(self, animated=False, interval=0.1):
        """
        Draw the plot onto the screen and initialize all controls.
        Support animation given a certain interval of seconds.
        """
        ax = self._figure.axes[0]
        self.pause()
        if animated:
            self.__animate_plot(
                ax, interval)
            # ax.set_animated(True)
            # self.after(500,lambda:self.__animate_plot(
            #     ax, interval))
        else:
            ax.plot(self.time, self.signal["samples"], color="blue")
            ax.grid(True)
            ax.set_xlabel("Time [s]")
            ax.set_ylabel("Amplitude")
            ax.set_xlim(0, 0.1*self.signal["N"]/self.signal["Fs"])
            ax.set_ylim(min(self.signal["samples"]),
                        max(self.signal["samples"]))

        # Initial draw
        self._figure.canvas.draw_idle()
        self._figure.canvas.flush_events()

    def __animate_plot(self, ax, interval):
        """
        Animates the drawing of the plot based on an interval of seconds
        """
        line = ax.plot([], [], color="blue")[0]

        def init():
            # ax.set_xlim(0, 0.1*self.signal["N"]/self.signal["Fs"])
            # ax.set_xlim(0, 1)
            ax.set_xlim(0, 0.02)
            ax.set_ylim(
                min(self.equalized_samples), max(self.equalized_samples))
            ax.set_xlabel("Time")
            ax.set_ylabel("Amplitude")
            ax.grid(True)
            return [line]

        def update(frame):
            try:
                if frame == int(self.signal["N"]/self.points_per_draw):
                    x = self.time
                    y = self.equalized_samples
                else:
                    x = self.time[:frame * self.points_per_draw]
                    y = self.equalized_samples[:frame * self.points_per_draw]

                # update view limits
                xmin,xmax = ax.get_xlim()
                if x[-1] > xmax:
                    xmin = xmin + (x[-1]-xmax) 
                    xmax = x[-1]
                    ax.set_xlim(xmin, xmax)
                    self._figure.canvas.draw_idle()
                
                self.current_frame = self.current_frame + 1
                
                # Always flush to give control back to the GUI event loop
                # and not freeze the app
                self._figure.canvas.flush_events()
                line.set_data(x, y)
                return [line]
            except Exception as e:
                print(e)

        # Setting the Interval too low messes up the the event loop
        # when there are multiple plots
        self._animation = FuncAnimation(self._figure, update,range(self.current_frame, int(self.signal["N"]/self.points_per_draw) + 1),
                                        init_func=init, interval=interval*1000, blit=True, repeat=False)
        # self._animation = FuncAnimation(self._figure, update, range(1, int(self.signal["N"]/100) + 1),
        #                                 init_func=init, interval=interval*1000, blit=True, repeat=True)

    def __mode_control(self, event):
        """
        Execute a function based on the current mode.
        Supported modes are zooming and panning.
        """
        mode = self.master.get_mode()

        if self.modes.get(mode) is not None:
            self.modes[mode](event)

    def pan(self, original_event):

        def release(new_event):
            self._figure.canvas.mpl_disconnect(self.drag_listener)
            self._figure.canvas.mpl_disconnect(self.release_listener)

            # Plot a new line with the same data
            # because for some reason the original line disappears
            # when zooming on a paused plot
            # x, y = self._figure.axes[0].get_lines()[0].get_data()
            # self._figure.axes[0].plot(x, y, color="blue")
            # self._figure.draw_artist(original_event.inaxes)
            self._figure.canvas.draw_idle()
            self._figure.canvas.flush_events()

            # Remove the newly created line but don't update the canvas
            # self._figure.axes[0].get_lines()[-1].remove()

        def drag(new_event):
            xdata, ydata = original_event.inaxes.get_lines()[0].get_data()

            # In case of scrolling outside the axis
            x = new_event.xdata or original_event.xdata
            y = new_event.ydata or original_event.ydata

            xmin, xmax = original_event.inaxes.get_xlim()
            ymin, ymax = original_event.inaxes.get_ylim()

            dx = original_event.xdata - x
            dy = original_event.ydata - y

            if not (xmin + dx < 0 or xmax + dx > xdata[-1]):
                original_event.inaxes.set_xlim(xmin + dx, xmax + dx)

            if not (ymin + dy < min(ydata) or ymax + dy > max(ydata)):
                original_event.inaxes.set_ylim(ymin + dy, ymax + dy)

            self._figure.canvas.draw_idle()

        self.drag_listener = self._figure.canvas.mpl_connect(
            "motion_notify_event", drag)
        self.release_listener = self._figure.canvas.mpl_connect(
            "button_release_event", release)

    def zoom_out(self, event):
        x, y = event.inaxes.get_lines()[0].get_data()
        # xmin, xmax = event.inaxes.get_xlim()
        
        event.inaxes.margins(2,2)
        event.inaxes.use_sticky_edges = False
        event.inaxes.autoscale_view(scalex=True,scaley=True)
        # event.inaxes.plot(x,y)
        self._figure.canvas.draw_idle()

    # Needs refactoring
    def zoom_in(self, event):
        xmin, xmax = event.inaxes.get_xlim()
        ymin, ymax = event.inaxes.get_ylim()

        # event.inaxes.set_xlim(xmin*0.5, xmax*0.5)
        # event.inaxes.set_ylim(ymin*0.5, ymax*0.5)

        if xmin == 0:
            event.inaxes.set_xlim(
                0, xmax / self.zoom_scale)
        # else:
        #     event.inaxes.set_xlim(
        #         xmin * self.zoom_scale, xmax / self.zoom_scale)

        # event.inaxes.set_ylim(
        #     ymin * self.zoom_scale, ymax / self.zoom_scale)

        # Plot a new line with the same data
        # because for some reason the original line disappears
        # when zooming on a paused plot
        # print(event.inaxes.get_lines()[-1].get_animated())
        # event.inaxes.plot(x, y, color="blue")

        self._figure.canvas.draw_idle()
        self._figure.canvas.flush_events()

        # Remove the newly created line but don't update the canvas
        event.inaxes.get_lines()[-1].remove()

    def pause(self):
        if self._animation:
            self._animation.event_source.stop()
            self._figure.axes[0].get_lines()[0].set_animated(False)
            self.playing = False
            self._figure.canvas.draw_idle()
            self._figure.canvas.flush_events()

    def play(self):
        if self._animation:
            self._figure.axes[0].get_lines()[0].set_animated(True)
            self._animation.event_source.start()
            self.playing = True
            self._figure.canvas.flush_events()

    def toggle_ax(self,ax):
        ax.set_visible(not ax.get_visible())
        self._figure.canvas.draw_idle()
        self._figure.canvas.flush_events()