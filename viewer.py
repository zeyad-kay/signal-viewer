import tkinter as tk
from matplotlib.pyplot import rcParams
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation


class Viewer(tk.Frame):
    """
    Visual component for viewing data on a Matplotlib Figure.
    """

    def __init__(self, master=None, samples={}, rows=1, columns=1):
        super().__init__(master,background="white")
        self.master = master
        self.zoom_scale = 2
        self.playing = True
        self.samples = samples
        self._animation = None
        self.modes = {
            "zoomIn": self.zoom_in,
            "zoomOut": self.zoom_out,
            "pan": self.pan
        }
        self.__create_figure(rows, columns)

    def __create_figure(self, rows, columns):
        """
        Create a matplotlib Figure and initialize the grid.
        """
        # inches to pixel conversion
        px = 1/rcParams['figure.dpi']
        # self._figure = Figure(figsize=((self.master.winfo_screenwidth(
        # ))*px, (self.master.winfo_screenheight())*px), constrained_layout=True)
        self._figure = Figure(figsize=(5, 5), constrained_layout=True)
        FigureCanvasTkAgg(self._figure, master=self)
        self._grid = self._figure.add_gridspec(rows, columns)
        self.columnconfigure(0, weight=1)
        self._figure.canvas.get_tk_widget().grid(row=0, column=0, sticky='nswe')

        self._figure.canvas.mpl_connect('axes_enter_event', self.listen)
        self._figure.canvas.mpl_connect(
            'axes_leave_event', lambda e: self._figure.canvas.mpl_disconnect(self.cid))

    def listen(self, e):
        self.cid = self._figure.canvas.mpl_connect(
            'button_press_event', self.__mode_control)

    def spectrogram(self, row, column):
        try:
            print("row: ", row)
            print("column: ", column)
            self._figure.add_subplot(self._grid[row, column]).specgram(
                self.samples["y"], self.samples["freq"])
            self._figure.canvas.draw_idle()
            self._figure.canvas.flush_events()
        except Exception as e:
            print(e)

    def plot(self, row, column, animated=False, interval=0.1):
        """
        Draw the plot onto the screen and initialize all controls.
        Support animation given a certain interval of seconds.
        """
        ax = self._figure.add_subplot(self._grid[row, column])

        if animated:
            self.__animate_plot(ax, interval)
        else:
            ax.plot(
                self.samples["x"], self.samples["y"], color="blue")
            ax.grid(True)
            ax.set_xlabel("Time")
            ax.set_ylabel("Amplitude")
            ax.set_xlim(0, self.samples["x"][1000])
            ax.set_ylim(
                min(self.samples["y"]), max(self.samples["y"]))

        # self._figure.add_subplot(self._grid[1, :])
        # Initial draw
        self._figure.canvas.draw_idle()

    def __animate_plot(self, ax, interval):
        """
        Animates the drawing of the plot based on an interval of seconds
        """
        line = ax.plot([], [], color="blue")[0]

        def init():
            line.axes.set_xlim(0, self.samples["x"][1000])
            line.axes.set_ylim(
                min(self.samples["y"]) * self.zoom_scale, max(self.samples["y"]) * self.zoom_scale)
            line.axes.set_xlabel("Time")
            line.axes.set_ylabel("Amplitude")
            line.axes.grid(True)
            return [line]

        def update(frame):
            try:
                if frame * 100 > self.samples["y"].__len__():
                    x = self.samples["x"]
                    y = self.samples["y"]
                else:
                    x = self.samples["x"][:frame * 100]
                    y = self.samples["y"][:frame * 100]

                # adjust scale
                xmin, xmax = self._figure.axes[0].get_xlim()
                ymin, ymax = self._figure.axes[0].get_ylim()
                scaled = False
                if x[-1] > xmax:
                    self._figure.axes[0].set_xlim(xmax-1, xmax + 2)
                    scaled = True
                # if y[-1] > ymax:
                #     self._figure.axes[0].set_ylim(ymax,y[-1] * self.zoom_scale)
                    # scaled = True
                # if y[-1] < ymin:
                #     self._figure.axes[0].set_ylim(y[-1] * self.zoom_scale , ymax)
                #     scaled = True
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
        self._animation = FuncAnimation(self._figure, update, frames=range(1, int(self.samples["y"].__len__()/100) + 1),
                                        init_func=init, interval=interval*1000, blit=True, repeat=False)
        # self._animation = FuncAnimation(self._figure, update,frames=range(900,self.samples["y"].__len__()),
        #     init_func=init, interval=interval*1000,blit=True,repeat=False)

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
            x, y = original_event.inaxes.get_lines()[0].get_data()
            original_event.inaxes.plot(x, y, color="blue")

            self._figure.canvas.draw_idle()
            self._figure.canvas.flush_events()

            # Remove the newly created line but don't update the canvas
            original_event.inaxes.get_lines()[-1].remove()

        def drag(new_event):
            # In case of scrolling outside the axis
            x = new_event.xdata or original_event.xdata
            y = new_event.ydata or original_event.ydata

            xmin, xmax = original_event.inaxes.get_xlim()
            ymin, ymax = original_event.inaxes.get_ylim()

            dx = original_event.xdata - x
            dy = original_event.ydata - y

            reached_xlimit = False
            
            if xmin + dx < self.samples["x"][0]:
                original_event.inaxes.set_xlim(self.samples["x"][0], xmax)
                reached_xlimit = True
            if xmax + dx > self.samples["x"][-1]:
                original_event.inaxes.set_xlim(xmin, self.samples["x"][-1])
                reached_xlimit = True
            if not reached_xlimit:
                original_event.inaxes.set_xlim(xmin + dx, xmax + dx)
            
            original_event.inaxes.set_ylim(ymin + dy, ymax + dy)


            self._figure.canvas.draw_idle()

        self.drag_listener = self._figure.canvas.mpl_connect(
            "motion_notify_event", drag)
        self.release_listener = self._figure.canvas.mpl_connect(
            "button_release_event", release)
    
    # Needs refactoring
    def zoom_out(self, event):
        ymin, ymax = event.inaxes.get_ylim()
        xmin, xmax = event.inaxes.get_xlim()

        reached_xlimit = False
        if xmax * self.zoom_scale > self.samples["x"][-1]:
            event.inaxes.set_xlim(0, self.samples["x"][-1])
            reached_xlimit = True

        if not reached_xlimit:
            event.inaxes.set_xlim(0, xmax * self.zoom_scale)
        
        # event.inaxes.set_ylim(
        #     ymin * self.zoom_scale, ymax * self.zoom_scale)

        # Plot a new line with the same data
        # because for some reason the original line disappears
        # when zooming on a paused plot
        x, y = event.inaxes.get_lines()[0].get_data()
        event.inaxes.plot(x, y, color="blue")

        self._figure.canvas.draw_idle()
        self._figure.canvas.flush_events()

        # Remove the newly created line but don't update the canvas
        event.inaxes.get_lines()[-1].remove()
    
    # Needs refactoring
    def zoom_in(self, event):
        xmin, xmax = event.inaxes.get_xlim()
        ymin, ymax = event.inaxes.get_ylim()

        reached_xlimit = False
        
        # if reached_xlimit:

        event.inaxes.set_xlim(
            xmin / self.zoom_scale, xmax / self.zoom_scale)
        # event.inaxes.set_ylim(
        #     ymin / self.zoom_scale, ymax / self.zoom_scale)

        # Plot a new line with the same data
        # because for some reason the original line disappears
        # when zooming on a paused plot
        x, y = event.inaxes.get_lines()[0].get_data()
        event.inaxes.plot(x, y, color="blue")

        self._figure.canvas.draw_idle()
        self._figure.canvas.flush_events()

        # Remove the newly created line but don't update the canvas
        event.inaxes.get_lines()[-1].remove()

    def pause(self):
        if self._animation:
            self._animation.event_source.stop()
            self.playing = False
            self._figure.canvas.flush_events()

    def play(self):
        if self._animation:
            self._animation.event_source.start()
            self.playing = True
            self._figure.canvas.flush_events()
