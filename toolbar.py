import tkinter as tk
from file_explorer import File_Explorer

class ToolBar(tk.Frame):
	def __init__(self,master=None):
		super().__init__(master,bg="white")
		self.master = master
		# open file button + the icon
		self.grid(row=0,column=5,sticky="ew")
		self.openImg = tk.PhotoImage(file="images/folder1.png")
		self.openButton = tk.Button(self , image=self.openImg, border=0, bg="white" , command=lambda : File_Explorer.open_file(master))
		self.openButton.grid(row=0 ,column=0,padx=5,pady=3)
		
		#save as button + the icon
		self.saveImg = tk.PhotoImage(file="images/floppy1.png")
		self.saveAsButton =tk.Button(self , image=self.saveImg, border=0, bg="white" , command=lambda : File_Explorer.save_file(master))
		self.saveAsButton.grid(row=0 ,column=1,padx=5,pady=3)
		
		# #scale button + the icon
		self.scaleImg = tk.PhotoImage(file="images/pan.png")
		self.scaleButton = tk.Button(self , image=self.scaleImg, border=0, bg="white" , command=lambda : self.master.set_mode("pan"))
		self.scaleButton.grid(row=0 ,column=2,padx=5,pady=3)
	
		self.zoomInImg = tk.PhotoImage(file="images/zoomIn.png")
		self.scaleButton = tk.Button(self , image=self.zoomInImg, border=0, bg="white" , command=lambda : self.master.set_mode("zoomIn"))
		self.scaleButton.grid(row=0 ,column=3,padx=5,pady=3)

		self.zoomOutImg = tk.PhotoImage(file="images/zoomOut.png")
		self.scaleButton = tk.Button(self , image=self.zoomOutImg, border=0, bg="white" , command=lambda : self.master.set_mode("zoomOut"))
		self.scaleButton.grid(row=0 ,column=4,padx=5,pady=3)	