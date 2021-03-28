import tkinter as tk
from file_explorer import File_Explorer
from helpers import read_file

class ToolBar(tk.Frame):
	def __init__(self,master=None):
		super().__init__(master,bg="#dad7d7")
		# open file button + the icon
		self.openImg = tk.PhotoImage(file="images/folder1.png")
		self.openButton = tk.Button(master , image=self.openImg , command=File_Explorer.browse_files)
		self.openButton.grid(row=0 ,column=1,padx=5)
		self.openButton.columnconfigure(1,weight=1)
		#save as button + the icon
		self.saveImg = tk.PhotoImage(file="images/floppy1.png")
		self.saveAsButton =tk.Button(master , image=self.saveImg , command=self.printing ,borderwidth=1)
		self.saveAsButton.grid(row=0 ,column=2,padx=5,pady=3)
		self.saveAsButton.columnconfigure(2,weight=1)
		# scale button + the icon
		self.scaleImg = tk.PhotoImage(file="images/pan.png")
		self.scaleButton = tk.Button(master , image=self.scaleImg , command=lambda : self.master.change_cursor("fleur"),borderwidth=1)
		self.scaleButton.grid(row=0 ,column=3,padx=5,pady=3)
		self.scaleButton.columnconfigure(3,weight=1)
	
		self.zoomInImg = tk.PhotoImage(file="images/zoomIn.png")
		self.scaleButton = tk.Button(master , image=self.zoomInImg , command=lambda : self.master.change_cursor("plus"),borderwidth=1)
		self.scaleButton.grid(row=0 ,column=4,padx=5,pady=3)
		self.scaleButton.columnconfigure(4,weight=1)

		self.zoomOutImg = tk.PhotoImage(file="images/zoomOut.png")
		self.scaleButton = tk.Button(master , image=self.zoomOutImg , command=lambda : self.master.change_cursor("circle"),borderwidth=1)
		self.scaleButton.grid(row=0 ,column=5,padx=5,pady=3)
		self.scaleButton.columnconfigure(5,weight=1)
		
		self.master.grid(row=0,column=4)

	def printing(self):
		print("printing")
	