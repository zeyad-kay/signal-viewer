import tkinter as tk
from file_explorer import File_Explorer

class ToolBar(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="white")
        self.master = master

        self.playImg = tk.PhotoImage(file="images/pause.png")
        self.playButton = tk.Button(
            self, image=self.playImg, bd=0, bg="white", command=lambda: self.toggle())
        self.playButton.grid(row=0, column=0, padx=5, pady=3)

        self.saveImg = tk.PhotoImage(file="images/floppy.png")
        self.saveAsButton = tk.Button(
            self, image=self.saveImg, border=0, bg="white", command=lambda: File_Explorer.save_file(master))
        self.saveAsButton.grid(row=0, column=1, padx=5, pady=3)

        self.scaleImg = tk.PhotoImage(file="images/pan.png")
        self.scaleButton = tk.Button(
            self, image=self.scaleImg, border=0, bg="white", command=lambda: self.master.set_mode("pan"))
        self.scaleButton.grid(row=0, column=2, padx=5, pady=3)

        self.zoomInImg = tk.PhotoImage(file="images/zoomIn.png")
        self.scaleButton = tk.Button(self, image=self.zoomInImg, border=0,
                                     bg="white", command=lambda: self.master.set_mode("zoomIn"))
        self.scaleButton.grid(row=0, column=3, padx=5, pady=3)

        self.zoomOutImg = tk.PhotoImage(file="images/zoomOut.png")
        self.scaleButton = tk.Button(self, image=self.zoomOutImg, border=0,
                                     bg="white", command=lambda: self.master.set_mode("zoomOut"))
        self.scaleButton.grid(row=0, column=4, padx=5, pady=3)

        self.deleteImg = tk.PhotoImage(file="images/trash.png")
        self.deleteButton = tk.Button(self, image=self.deleteImg, border=0,
                                      bg="white", command=lambda: self.master.delete_tab())
        self.deleteButton.grid(row=0, column=5, padx=5, pady=3)

    def toggle(self):
        if self.master.viewer.playing:
            self.master.viewer.pause()
            self.playImg = tk.PhotoImage(file="images/play.png")
        else:
            self.master.viewer.play()
            self.playImg = tk.PhotoImage(file="images/pause.png")
        self.playButton["image"] = self.playImg