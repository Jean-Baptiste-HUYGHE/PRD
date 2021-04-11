from tkinter import *
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo

from Controller.FormWindowController import FormWindowController
from View.OptionsWindow import OptionsWindow

"""@package View
This module manages the different windows of the application.
"""


class FormWindow(Toplevel):
	"""
    Class for the window to create a new connectome.
    """

	def __init__(self, parent, **kwargs):
		"""
        Init function for the form window
        :param parent: the parent window
        :param kwargs: the arguments for the tkinter.Toplevel superclass
        """
		super().__init__(**kwargs)
		self.controller = FormWindowController(self, parent)
		self.parent = parent
		self.resizable(0, 0)
		self.title("New Connectome")
		self.options = None

		self.matrixname = ""
		self.atlasname = ""

		self.color = StringVar()

		self.main_frame = Frame(self, width=200, height=400)
		self.main_frame.grid(row=0, column=0, padx=10, pady=5)

		self.name_label = Label(self.main_frame, text="Name:")
		self.name_label.grid(row=1, column=0, padx=5, pady=5, sticky='news')
		self.name_field = Entry(self.main_frame)
		self.name_field.grid(row=1, column=1, padx=5, pady=5, sticky='news')
		self.color_label = Label(self.main_frame, text="Color:")
		self.color_label.grid(row=2, column=0, padx=5, pady=5, sticky='news')
		colors = ("grey", "red", "blue", "green", "black", "yellow")
		self.color_combo = ttk.Combobox(self.main_frame, state="readonly", values=colors, textvariable=self.color)
		self.color_combo.grid(row=2, column=1, padx=5, pady=5, sticky='news')
		self.color_combo.current(0)

		self.matrix_label = Label(self.main_frame, text="Matrix:")
		self.matrix_label.grid(row=3, column=0, padx=5, pady=5, sticky='news')
		self.matrix_field = Entry(self.main_frame, state='readonly')
		self.matrix_field.grid(row=3, column=1, padx=5, pady=5, sticky='news')
		self.matrix_button = Button(self.main_frame, text="Select", fg="black", command=lambda f=1: self.selectMatrix())
		self.matrix_button.grid(row=3, column=2, padx=5, pady=5, sticky='news')

		self.atlas_label = Label(self.main_frame, text="Atlas:")
		self.atlas_label.grid(row=4, column=0, padx=5, pady=5, sticky='news')
		self.atlas_field = Entry(self.main_frame, state='readonly')
		self.atlas_field.grid(row=4, column=1, padx=5, pady=5, sticky='news')
		self.atlas_button = Button(self.main_frame, text="Select", fg="black", command=lambda f=1: self.selectAtlas())
		self.atlas_button.grid(row=4, column=2, padx=5, pady=5, sticky='news')
		self.button_OK = Button(self.main_frame, text="OK", fg="black", command=lambda f=1: self.validate())
		self.button_OK.grid(row=5, column=1, padx=5, pady=5, sticky='news')
		self.button_cancel = Button(self.main_frame, text="Cancel", fg="black", command=lambda f=1: self.destroy())
		self.button_cancel.grid(row=5, column=2, padx=5, pady=5, sticky='news')

		self.protocol("WM_DELETE_WINDOW", self.destroy)
		self.config()
		self.mainloop()

	def selectMatrix(self):
		"""
		Opens a filedialog to select a matrix to load and writes the file path into the corresponding textfield
		:return: None
		"""
		self.matrixname = filedialog.askopenfilename(initialdir="/", title="Select matrix file",
		                             defaultextension=".txt",
		                                             filetypes=(("EDGE files", "*.edge"), ("Text files", "*.txt"),
		                                                        ("CSV files", "*.csv")))
		self.matrix_field.config(state="normal")
		self.matrix_field.delete(0, END)
		self.matrix_field.insert(0, self.matrixname)
		self.matrix_field.config(state="readonly")
		self.lift()

	def selectAtlas(self):
		"""
		Opens a filedialog to select an atlas to load and writes the file path into the corresponding textfield
		:return: None
		"""
		self.atlasname = filedialog.askopenfilename(initialdir="/", title="Select atlas file",
		                             defaultextension=".csv",
		                                             filetypes=(("NODE files", "*.node"), ("Text files", "*.txt"),
		                                                        ("CSV files", "*.csv"), ("XML files", "*.xml")))
		self.atlas_field.config(state="normal")
		self.atlas_field.delete(0, END)
		self.atlas_field.insert(0, self.atlasname)
		self.atlas_field.config(state="readonly")
		self.lift()

	def validate(self):
		"""
		Checks the mandatory information and sends it to the parent if it is correct.
		:return: None
		"""
		if not self.name_field.get() or not self.matrix_field.get() or not self.atlas_field.get():
			showinfo("Missing information", "Please enter a name for the graph and select a matrix and an atlas.")
			self.lift()
		else:
			self.withdraw()
			OptionsWindow(self)

	def createObject(self):
		"""
		Creates the connectome object
		:return: None
		"""
		connectomeobject = self.controller.createConnectomeObject(self.options)
		self.destroy()
		self.parent.controller.setConnectomeObject(connectomeobject)

