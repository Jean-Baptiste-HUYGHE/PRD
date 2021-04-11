import tkinter.tix as Tix
from tkinter import *
from tkinter import ttk

from Controller import MainWindowController

"""@package View
This module manages the different windows of the application.
"""


class VisualizeOptionWindow(Toplevel):
	"""
    Class for the window to select graph options.
    """

	def __init__(self, parent, action, **kwargs):
		"""
		Init function for the option window
		:param parent: the parent window
		:param kwargs: the arguments for the tkinter.Toplevel superclass
		"""
		super().__init__(**kwargs)
		self.parent = parent
		self.resizable(0, 0)
		self.title("Visualization options")
		self.action = action

		self.option = StringVar()

		self.main_frame = Frame(self, width=200, height=400)
		self.main_frame.grid(row=0, column=0, padx=10, pady=5)

		if self.action == "viz":
			self.option_label = Label(self.main_frame, text="Visualization type:", font=("Courier", 12))
			self.option_label.grid(row=1, column=0, padx=5, pady=5, sticky='news')
			options = ("default", "left", "right", "unlinked")
		else:
			self.option_label = Label(self.main_frame, text="Graph type:", font=("Courier", 12))
			self.option_label.grid(row=1, column=0, padx=5, pady=5, sticky='news')
			options = ("default", "left", "right")
		self.color_combo = ttk.Combobox(self.main_frame, state="readonly", values=options, textvariable=self.option)
		self.color_combo.grid(row=1, column=1, padx=5, pady=5, sticky='news')
		self.color_combo.current(0)

		self.button_OK = Button(self.main_frame, text="OK", fg="black", command=lambda f=1: self.validate())
		self.button_OK.grid(row=2, column=0, padx=5, pady=5, sticky='news')
		self.button_cancel = Button(self.main_frame, text="Cancel", fg="black", command=lambda f=1: self.destroy())
		self.button_cancel.grid(row=2, column=1, padx=5, pady=5, sticky='news')

	def validate(self):
		"""
		Sends the option selected to the parent window.
		:return: None
		"""
		if self.action == "viz":
			self.parent.controller.visualizeConnectome(self.option.get())
		elif self.action == "build":
			self.parent.controller.createConnectomeGraph(self.option.get())
		self.destroy()


