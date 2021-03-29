import tkinter as tk
from file_explorer import File_Explorer

class ToolBar(tk.Frame):
	def __init__(self,master=None):
		super().__init__(master,bg="white")
		self.master = master
		# open file button + the icon
		self.grid(row=0,column=5,sticky="ew")
		self.openImg = tk.PhotoImage(file="images/folder1.png")
		self.openButton = tk.Button(self , image=self.openImg , command=lambda : File_Explorer.browse_files(master))
		self.openButton.grid(row=0 ,column=0,padx=5,pady=3)
		
		#save as button + the icon
		self.saveImg = tk.PhotoImage(file="images/floppy1.png")
		self.saveAsButton =tk.Button(self , image=self.saveImg , command=self.printing ,borderwidth=1)
		self.saveAsButton.grid(row=0 ,column=1,padx=5,pady=3)
		
		# #scale button + the icon
		self.scaleImg = tk.PhotoImage(file="images/pan.png")
		self.scaleButton = tk.Button(self , image=self.scaleImg , command=lambda : self.master.change_cursor("fleur"),borderwidth=1)
		self.scaleButton.grid(row=0 ,column=2,padx=5,pady=3)
	
		self.zoomInImg = tk.PhotoImage(file="images/zoomIn.png")
		self.scaleButton = tk.Button(self , image=self.zoomInImg , command=lambda : self.master.change_cursor("plus"),borderwidth=1)
		self.scaleButton.grid(row=0 ,column=3,padx=5,pady=3)

		self.zoomOutImg = tk.PhotoImage(file="images/zoomOut.png")
		self.scaleButton = tk.Button(self , image=self.zoomOutImg , command=lambda : self.master.change_cursor("circle"),borderwidth=1)
		self.scaleButton.grid(row=0 ,column=4,padx=5,pady=3)
		

	def printing(self):
		print("printing")
	