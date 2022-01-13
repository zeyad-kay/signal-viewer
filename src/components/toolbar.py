import tkinter as tk
from tkinter import ttk
from os.path import join, dirname 
from .file_explorer import File_Explorer

class ToolBar(tk.Frame):
    def __init__(self, master=None, viewer=None):
        super().__init__(master, bg="white")
        self.master = master
        self.rowconfigure(0, weight=1)
        self.viewer = viewer
        self.playImg = tk.PhotoImage(file=join(dirname(__file__),"icons","pause.png"))
        self.playButton = tk.Button(
            self, image=self.playImg, bd=0, bg="white", command=lambda: self.toggle_play())
        self.playButton.grid(row=0, column=0, padx=5, pady=3)

        self.saveImg = tk.PhotoImage(file=join(dirname(__file__),"icons","floppy.png"))
        self.saveAsButton = tk.Button(
            self, image=self.saveImg, border=0, bg="white", command=lambda: File_Explorer.save_file(master))
        self.saveAsButton.grid(row=0, column=1, padx=5, pady=3)

        self.scaleImg = tk.PhotoImage(file=join(dirname(__file__),"icons","pan.png"))
        self.scaleButton = tk.Button(
            self, image=self.scaleImg, border=0, bg="white", command=lambda: self.master.set_mode("pan"))
        self.scaleButton.grid(row=0, column=2, padx=5, pady=3)

        self.zoomInImg = tk.PhotoImage(file=join(dirname(__file__),"icons","zoomIn.png"))
        self.scaleButton = tk.Button(self, image=self.zoomInImg, border=0,
                                     bg="white", command=lambda: self.master.set_mode("zoomIn"))
        self.scaleButton.grid(row=0, column=3, padx=5, pady=3)

        self.zoomOutImg = tk.PhotoImage(file=join(dirname(__file__),"icons","zoomOut.png"))
        self.scaleButton = tk.Button(self, image=self.zoomOutImg, border=0,
                                     bg="white", command=lambda: self.master.set_mode("zoomOut"))
        self.scaleButton.grid(row=0, column=4, padx=5, pady=3)

        self.deleteImg = tk.PhotoImage(file=join(dirname(__file__),"icons","trash.png"))
        self.deleteButton = tk.Button(self, image=self.deleteImg, border=0,
                                      bg="white", command=lambda: self.master.delete_tab())
        self.deleteButton.grid(row=0, column=5, padx=5, pady=3)
        
        self.spectrogram_on = tk.IntVar()
        self.spectrogram_on.set(1)
        self.spectrogramButton = tk.Checkbutton(self,variable=self.spectrogram_on,text="spectrogram",onvalue=1,offvalue=0, bg="white",command=lambda: self.toggle_spectrograms())
        self.spectrogramButton.grid(row=0, column=6, padx=5, pady=3)
        
        
        self.selected_color = tk.StringVar()
        self.selected_color.set("rainbow")
        self.spectrogramColor = ttk.Combobox(self,textvariable=self.selected_color)
        self.spectrogramColor["values"] = ("rainbow","spring","Greens","Blues","Reds","plasma","pink","gray")
        self.spectrogramColor.bind('<<ComboboxSelected>>', lambda e: self.color_spectrograms())
        self.spectrogramColor.grid(row=0, column=7, padx=5, pady=3)


    def color_spectrograms(self):
        self.viewer.set_cmap(self.selected_color.get())

    def toggle_spectrograms(self):
        self.viewer.toggle_ax(self.viewer._figure.axes[1])
        self.viewer.toggle_ax(self.viewer._figure.axes[3])
    
    def toggle_play(self):
        if self.viewer.playing:
            self.viewer.pause()
            self.playImg = tk.PhotoImage(file=join(dirname(__file__),"icons","play.png"))
        else:
            self.viewer.play()
            self.playImg = tk.PhotoImage(file=join(dirname(__file__),"icons","pause.png"))
        self.playButton["image"] = self.playImg