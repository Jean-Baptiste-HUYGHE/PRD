import tkinter
from tkinter import *
from tkinter.ttk import Treeview

from Controller.MainWindowController import MainWindowController

"""@package View
This module manages the different windows of the application.
"""


class MainWindow(Frame):
	"""
	Main window of the application. Displayed upon launch.
	"""

	def __init__(self, root, **kwargs):
		"""
        Init function for the main window
		:param root: the Tkinter root
		:param kwargs: the arguments for the tkinter.Frame superclass
		"""
		super().__init__(**kwargs)
		self.mainframe = tkinter.Frame(root, width=800, height=500, borderwidth=5)
		self.controller = MainWindowController(self)
		self.root = root
		root.resizable(0, 0)
		self.mainframe.grid(row=0, column=0, padx=10, pady=5)
		self.mainframe.grid_propagate(0)

		self.left_frame = Frame(self.mainframe, width=360, height=480)
		self.left_frame.grid(row=0, column=0, padx=10, pady=5, sticky='news')
		self.left_frame.grid_propagate(0)

		self.right_frame = Frame(self.mainframe, width=400, height=480, bg='lightgrey')
		self.right_frame.grid(row=0, column=1, padx=10, pady=5, sticky='news')
		self.right_frame.grid_propagate(0)
		self.right_frame.columnconfigure(0, weight=1)
		self.right_frame.columnconfigure(1, weight=0)
		self.right_frame.rowconfigure(0, weight=1)
		self.right_frame.rowconfigure(1, weight=0)

		root.title("Main Window")
		self.menubar = Menu(root)
		self.filemenu = Menu(self.menubar, tearoff=0)
		self.filemenu.add_command(label="New", command=lambda f=1: self.controller.newConnectomeFile(self))
		self.filemenu.add_command(label="Open", command=lambda f=1: self.controller.openConnectomeGraph())
		self.filemenu.add_command(label="Save", state=DISABLED, command=lambda f=1: self.controller.saveConnectomeGraph())
		self.filemenu.add_command(label="Save As", state=DISABLED, command=lambda f=1: self.controller.saveConnectomeGraphAs())

		self.comparemenu = Menu(self.menubar, tearoff=0)
		self.comparemenu.add_command(label="Compare graphs", state=DISABLED, command=lambda f=1: self.controller.compareGraphs())

		self.menubar.add_cascade(label="File", menu=self.filemenu)
		self.menubar.add_cascade(label="Compare", menu=self.comparemenu)

		self.button_graph = Button(self.left_frame, text="Build the graph", fg="black", state=DISABLED,
		                           command=lambda f=1: self.controller.askGraphOptions(self))
		self.button_graph.grid(row=1, column=0, padx=5, pady=5, sticky='news')

		self.button_display = Button(self.left_frame, text="Display graph informations", fg="black", state=DISABLED,
		                             command=lambda f=1: self.controller.infosConnectome(self.controller.model))
		self.button_display.grid(row=2, column=0, padx=5, pady=5, sticky='news')

		self.button_addinfo = Button(self.left_frame, text="Set connectome options", fg="black", state=DISABLED,
									command=lambda f=1: self.controller.addInfo())
		self.button_addinfo.grid(row=3, column=0, padx=5, pady=5, sticky='news')

		self.button_visualize = Button(self.left_frame, text="Visualize connectome", fg="black", state=DISABLED,
		                               command=lambda f=1: self.controller.askVisualizationOptions(self))
		self.button_visualize.grid(row=4, column=0, padx=5, pady=5, sticky='news')

		self.listConnectomes = Treeview(self.right_frame, selectmode="browse")
		self.listConnectomes.column("#0", width=400, minwidth=400, stretch=tkinter.NO)
		self.listConnectomes.heading("#0", text="Name", anchor=tkinter.W)
		self.listConnectomes.grid(row=0, column=0, padx=5, pady=5, sticky='news')
		self.listConnectomes.bind("<Double-Button-1>", self.controller.loadConnectomeFromList)
		self.listConnectomes.bind("<Button-3>", self.controller.askDelete)

		self.lift()
		root.protocol("WM_DELETE_WINDOW", root.destroy)
		root.config(menu=self.menubar)
		root.mainloop()

	def refresh(self):
		"""
		Refreshes the window.
		:return: None
		"""
		self.root.resizable(1, 1)
		self.root.geometry("800x500")
		self.root.resizable(0, 0)
		self.menubar.update()




