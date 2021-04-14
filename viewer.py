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
        self.signal = signal
        self.time = np.linspace(0, self.signal["samples"].__len__(
        ) * 1/self.signal["Fs"], self.signal["samples"].__len__())

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
        # self._grid = self._figure.add_gridspec(rows, columns)
        self._figure.canvas.get_tk_widget().grid(row=0, column=0, sticky='nswe')

        self._figure.canvas.mpl_connect('axes_enter_event', self.listen)
        self._figure.canvas.mpl_connect(
            'axes_leave_event', lambda e: self._figure.canvas.mpl_disconnect(self.cid))

    def listen(self, e):
        self.cid = self._figure.canvas.mpl_connect(
            'button_press_event', self.__mode_control)
    
    def update_samples(self,new_samples):
        self.signal["samples"] = new_samples
        self._figure.axes[1].clear()
        self.spectrogram()

    def spectrogram(self):
        try:
            self._figure.axes[1].specgram(self.signal["samples"], Fs=self.signal["Fs"])
            # self._figure.add_subplot(self._grid[row, column]).specgram(
            #     samples, Fs=Fs)
            # self._figure.add_subplot(self._grid[row, column]).specgram(
            #     self.samples["y"], Fs=self.samples["Fs"])
            self._figure.canvas.draw_idle()
            self._figure.canvas.flush_events()
        except Exception as e:
            print(e)

    def plot(self, animated=False, interval=0.1):
        """
        Draw the plot onto the screen and initialize all controls.
        Support animation given a certain interval of seconds.
        """
        # ax = self._figure.add_subplot(self._grid[row, column])
        ax = self._figure.axes[0]
        if animated:
            # ax.set_animated(True)
            self.__animate_plot(ax, self.time, self.signal["samples"], interval)
        else:
            ax.plot(self.time, self.signal["samples"], color="blue")
            ax.grid(True)
            ax.set_xlabel("Time [s]")
            ax.set_ylabel("Amplitude")
            ax.set_xlim(0, self.time[1000])
            ax.set_ylim(min(self.signal["samples"]), max(self.signal["samples"]))

        # self._figure.add_subplot(self._grid[1, :])
        # Initial draw
        self._figure.canvas.draw_idle()

    def __animate_plot(self, ax, time, samples, interval):
        """
        Animates the drawing of the plot based on an interval of seconds
        """
        line = ax.plot([], [], color="blue")[0]

        def init():
            ax.set_xlim(0, 1)
            ax.set_ylim(
                min(samples) * self.zoom_scale, max(samples) * self.zoom_scale)
            ax.set_xlabel("Time")
            ax.set_ylabel("Amplitude")
            ax.grid(True)
            return [line]

        def update(frame):
            try:
                if frame >= time.__len__()/100:
                    x = time
                    y = samples
                else:
                    x = time[:frame * 100]
                    y = samples[:frame * 100]

                # adjust scale
                xmax = ax.get_xlim()[1]
                if x[-1] == time[-1]:
                    ax.set_xlim(xmax, x[-1])
                    # self.pause()
                    # print(ax.get_xlim())
                    # return
                    self._figure.canvas.draw_idle()
                elif x[-1] > xmax:
                    ax.set_xlim(xmax, x[-1] + 1)
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
        self._animation = FuncAnimation(self._figure, update, range(1, int(self.signal["samples"].__len__()/100) + 1),
                                        init_func=init, interval=interval*1000, blit=True, repeat=False)

    def __mode_control(self, event):
        """
        Execute a function based on the current mode.
        Supported modes are zooming and panning.
        """
        mode = self.master.get_mode()

        if self.modes.get(mode) is not None:
            self.modes[mode](event)

    def pan(self, original_event):
        # print(self._figure.axes[0].get_lines()[-1].get_animated())
        def release(new_event):
            self._figure.canvas.mpl_disconnect(self.drag_listener)
            self._figure.canvas.mpl_disconnect(self.release_listener)

            # Plot a new line with the same data
            # because for some reason the original line disappears
            # when zooming on a paused plot
            x, y = self._figure.axes[0].get_lines()[0].get_data()
            self._figure.axes[0].plot(x, y, color="blue")

            self._figure.canvas.draw_idle()
            self._figure.canvas.flush_events()

            # Remove the newly created line but don't update the canvas
            self._figure.axes[0].get_lines()[-1].remove()

        def drag(new_event):
            xdata, ydata = original_event.inaxes.get_lines()[0].get_data()

            # In case of scrolling outside the axis
            x = new_event.xdata or original_event.xdata
            y = new_event.ydata or original_event.ydata

            xmin, xmax = original_event.inaxes.get_xlim()
            ymin, ymax = original_event.inaxes.get_ylim()

            dx = original_event.xdata - x
            dy = original_event.ydata - y

            reached_xlimit = False
            reached_ylimit = False

            if xmin + dx < xdata[0]:
                original_event.inaxes.set_xlim(xdata[0], xmax)
                reached_xlimit = True
            # if xmax + dx > xdata[-1]:
            #     original_event.inaxes.set_xlim(xmin, xdata[-1])
            #     reached_xlimit = True
            if not reached_xlimit:
                original_event.inaxes.set_xlim(xmin + dx, xmax + dx)

            # if ymin + dy < min(ydata):
            #     original_event.inaxes.set_ylim(min(ydata), ymax)
            #     reached_ylimit = True
            # if ymax + dy > max(ydata):
            #     original_event.inaxes.set_ylim(ymin, max(ydata))
            #     reached_ylimit = True
            # if not reached_ylimit:
            original_event.inaxes.set_ylim(ymin + dy, ymax + dy)

            self._figure.canvas.draw_idle()

        self.drag_listener = self._figure.canvas.mpl_connect(
            "motion_notify_event", drag)
        self.release_listener = self._figure.canvas.mpl_connect(
            "button_release_event", release)

    def zoom_out(self, event):
        new_xmin = 0
        new_xmax = 0
        new_ymin = 0
        new_ymax = 0

        ymin, ymax = event.inaxes.get_ylim()
        xmin, xmax = event.inaxes.get_xlim()

        if xmax * self.zoom_scale > self.samples["x"][-1]:
            new_xmax = self.samples["x"][-1]
        else:
            new_xmax = xmax * self.zoom_scale

        new_xmin = xmin / self.zoom_scale

        if ymax > 0:
            if ymax * self.zoom_scale > max(self.samples["y"]):
                new_ymax = max(self.samples["y"])
            else:
                new_ymax = ymax * self.zoom_scale
        else:
            if ymax / self.zoom_scale > max(self.samples["y"]):
                new_ymax = max(self.samples["y"])
            else:
                new_ymax = ymax / self.zoom_scale
        if ymin < 0:
            if ymin * self.zoom_scale < min(self.samples["y"]):
                new_ymin = min(self.samples["y"])
            else:
                new_ymin = ymin * self.zoom_scale
        else:
            if ymin / self.zoom_scale < min(self.samples["y"]):
                new_ymin = min(self.samples["y"])
            else:
                new_ymin = ymin / self.zoom_scale

        event.inaxes.set_xlim(new_xmin, new_xmax)
        event.inaxes.set_ylim(new_ymin, new_ymax)

        # Plot a new line with the same data
        # because for some reason the original line disappears
        # when zooming on a paused plot
        x, y = self._figure.axes[0].get_lines()[0].get_data()
        self._figure.axes[0].plot(x, y, color="blue")

        self._figure.canvas.draw_idle()
        self._figure.canvas.flush_events()

        # Remove the newly created line but don't update the canvas
        self._figure.axes[0].get_lines()[-1].remove()

    # Needs refactoring
    def zoom_in(self, event):
        xmin, xmax = event.inaxes.get_xlim()
        ymin, ymax = event.inaxes.get_ylim()

        event.inaxes.set_xlim(xmin*0.5, xmax*0.5)
        event.inaxes.set_ylim(ymin*0.5, ymax*0.5)

        # if xmin == 0:
        #     event.inaxes.set_xlim(
        #         event.xdata * self.zoom_scale, xmax / self.zoom_scale)
        # else:
        #     event.inaxes.set_xlim(
        #         xmin * self.zoom_scale, xmax / self.zoom_scale)

        # event.inaxes.set_ylim(
        #     ymin * self.zoom_scale, ymax / self.zoom_scale)

        # Plot a new line with the same data
        # because for some reason the original line disappears
        # when zooming on a paused plot
        # print(event.inaxes.get_lines()[-1].get_animated())
        x, y = self._figure.axes[0].get_lines()[0].get_data()
        event.inaxes.plot(x, y, color="blue")

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