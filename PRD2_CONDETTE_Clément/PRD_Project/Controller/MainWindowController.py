import ntpath
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showinfo

import networkx

from Connectome.ConnectomeObject import ConnectomeObject
from View.DisplayWindow import DisplayWindow
from View.FormWindow import FormWindow
from View.OptionsWindow import OptionsWindow
from View.VisualizeOptionWindow import VisualizeOptionWindow
from Visualisation.ConnectomeVisualizer import ConnectomeVisualizer

"""@package Controller
This module manages the controller part of the windows displayed by the application.
"""


class MainWindowController:
	"""
	Controller class of the main window of the application.
	"""

	def __init__(self, view):
		"""
		Init function for the main window controller
		:param view: the window to control
		"""
		self.model = ConnectomeObject("")
		self.graphsLoaded = dict()
		self.view = view
		self.visualizer = ConnectomeVisualizer()
		self.matrixName = None
		self.atlasName = None
		self.graphName = None
		self.filename = ""

	def createConnectomeGraph(self, option):
		"""
		Creates a connectomeGraph object from a loaded matrix and atlas and updates the graph of
		the selected object in the list if there is one.
		:return: None
		"""
		if self.model.atlasReader.filename and self.model.matrixReader.filename:
			success = self.model.loadConnectomeAtlasMatrix(option)
			if success:
				self.view.button_addinfo.config(state="normal")
				self.view.button_visualize.config(state="normal")
				self.view.button_display.config(state="normal")
				self.view.filemenu.entryconfigure(3, state="normal")
			else:
				showinfo("Error generating the graph",
				         "An error has occured, please try loading a new connectome.")
		else:
			self.model.reloadGraph(self.model.connectomegraph.options)
			success = self.model.loadSubGraph(option)
			if success:
				self.view.button_addinfo.config(state="normal")
				self.view.button_visualize.config(state="normal")
				self.view.button_display.config(state="normal")
				self.view.filemenu.entryconfigure(3, state="normal")
			else:
				showinfo("Error generating the graph",
				         "An error has occured, please try loading a new connectome.")

	def askGraphOptions(self, parent):
		"""
		Asks for the type of graph to be built.
		:return: None
		"""
		VisualizeOptionWindow(parent, "build")

	def setConnectomeObject(self, connectomeobject):
		"""
		Sets the connectome object in parameter as the current object used by the application.
		:param connectomeobject: the new object to set as the current object
		:return: None
		"""
		self.model = connectomeobject
		idcon = self.view.listConnectomes.insert("", "end", id=len(self.graphsLoaded), text=self.model.name)
		self.graphsLoaded[idcon] = self.model
		self.view.listConnectomes.selection_set(idcon)
		self.view.button_graph.config(state="normal")
		self.view.button_visualize.config(state="disabled")
		self.view.button_addinfo.config(state="disabled")
		self.view.button_display.config(state="disabled")

	def visualizeConnectome(self, option):
		"""
		Opens a visualization window for the current object.
		:return: None
		"""
		self.visualizer.visualizeConnectomeGraph(self.model, viztype=option)
		self.view.refresh()

	def askVisualizationOptions(self, parent):
		"""
		Opens a visualization option window.
		:return: None
		"""
		if self.model.connectomegraph.type == "default":
			VisualizeOptionWindow(parent, "viz")
		else:
			self.visualizeConnectome("default")

	def newConnectomeFile(self, parent):
		"""
		Opens a form window to give the informations to load a new connectome.
		:param parent: the parent window
		:return: None
		"""
		FormWindow(parent)

	def openConnectomeGraph(self):
		"""
		Asks for a readable file containing a connectome and initialize the current connectome object with a graph
		constructed from this connectome file.
		:return: None
		"""
		self.filename = filedialog.askopenfilename(initialdir="/", title="Select connectome file", defaultextension=".graphml",
								filetypes=(("GraphML files", "*.graphml"), ("GXL files", "*.gxl")))
		if self.filename:
			self.model = ConnectomeObject("")
			if self.filename.endswith(".graphml"):
				head, self.graphName = ntpath.split(self.filename)
				self.graphName = self.graphName.split('.')[0]
				self.model.graphReader.setFileName(self.filename)
				self.model.connectomegraph = self.model.graphReader.readGraphML()
			elif self.filename.endswith(".gxl"):
				head, self.graphName = ntpath.split(self.filename)
				self.graphName = self.graphName.split('.')[0]
				self.model.graphReader.setFileName(self.filename)
				self.model.connectomegraph = self.model.graphReader.readGXL()
			if self.model.connectomegraph.graph.is_directed():
				self.model.connectomegraph.options['directed'] = True
			if networkx.is_weighted(self.model.connectomegraph.graph):
				self.model.connectomegraph.options['weighted'] = True
			if not list(networkx.isolates(self.model.connectomegraph.graph)):
				self.model.connectomegraph.options['unlinked'] = True
			self.model.name = self.graphName
			idcon = self.view.listConnectomes.insert("", "end", id=len(self.graphsLoaded), text=self.model.name)
			self.graphsLoaded[idcon] = self.model
			self.view.listConnectomes.selection_set(idcon)
			self.model.connectomegraph.type = "default"
			tk.messagebox.showinfo("Opened", "The connectome has been loaded and the corresponding graph has been built."
			                                 " \n Press the \"Build graph\" button to build it as a subgraph.")
			self.view.button_display.config(state="normal")
			self.view.button_visualize.config(state="normal")
			self.view.button_addinfo.config(state="normal")
			self.view.button_graph.config(state="normal")
			self.view.filemenu.entryconfigure(2, state="normal")
			self.view.filemenu.entryconfigure(3, state="normal")

	def saveConnectomeGraph(self):
		"""
		Save the current connectome in a graphml or gxl file.
		If the connectome is not from an already established file and has no filename, asks for a filename beforehand.
		:return: the filename
		"""
		result = None
		if self.filename == "":
			result = self.saveConnectomeGraphAs()
		else:
			self.model.graphWriter.setFileName(self.filename)
			if self.filename.endswith(".graphml"):
				result = self.model.graphWriter.writeGraphML(self.model.connectomegraph)
			elif self.filename.endswith(".gxl"):
				result = self.model.graphWriter.writeGXL(self.model.connectomegraph)
		if result is not None:
			tk.messagebox.showinfo("Save", "File saved as " + str(result))
		else:
			tk.messagebox.showerror("Save", "The save encountered a problem. Please try again.")
		return result

	def saveConnectomeGraphAs(self):
		"""
		Asks for a filename and saves the connectome into the specified file.
		:return: the filename
		"""
		self.filename = filedialog.asksaveasfilename(initialdir="/", title="Save", defaultextension=".graphml",
								filetypes=(("GraphML files", "*.graphml"), ("GXL files", "*.gxl")))
		self.model.graphWriter.setFileName(self.filename)
		result = None
		if self.filename.endswith(".graphml"):
			result = self.model.graphWriter.writeGraphML(self.model.connectomegraph)
		elif self.filename.endswith(".gxl"):
			result = self.model.graphWriter.writeGXL(self.model.connectomegraph)
		if result is not None:
			tk.messagebox.showinfo("Save", "File saved as " + str(result) + ".")
		else:
			tk.messagebox.showerror("Save", "The save encountered a problem. Please try again.")
		return result

	def infosConnectome(self, model):
		"""
		Displays informations of the graph in a text format.
		:param model: the connectome to display
		:return: None
		"""
		DisplayWindow(model)

	def compareGraphs(self):
		"""
		Opens the graph comparison window.
		:return: None
		"""
		pass

	def addInfo(self):
		"""
		Calculates extra informations for the current graph.
		:return: None
		"""
		result = tk.messagebox.askokcancel("Options", "Add extra information to the graph?")
		if result:
			OptionsWindow(self)

	def checkAndUpdate(self, smallworld):
		"""
		Check the options and modify the graph accordingly.
		:param smallworld: boolean representing the smallworld option
		:return: None
		"""
		options = self.model.connectomegraph.options
		if smallworld:
			result = tk.messagebox.askyesno("Smallworldness", "Are you sure you want to calculate the smallworldness coefficient? "
			                                                  "(This operation may take a long time)")
			if result:
				self.model.connectomegraph.options['smallworld'] = True
			else:
				self.model.connectomegraph.options['smallworld'] = False
		self.model.reloadGraph(options)

	def loadConnectomeFromList(self, event):
		"""
		Takes a connectome from the displayed list and sets the corresponding connectome from the loaded connectomes
		as the current.
		:param event: the click event
		:return: None
		"""
		iid = self.view.listConnectomes.identify_row(event.y)
		if iid:
			self.view.listConnectomes.selection_set(iid)
			self.model = self.graphsLoaded[str(self.view.listConnectomes.selection()[0])]
			if networkx.is_empty(self.model.connectomegraph.graph):
				self.view.button_graph.config(state="normal")
				self.view.button_display.config(state="disabled")
				self.view.button_visualize.config(state="disabled")
			else:
				self.view.button_graph.config(state="disabled")
				self.view.button_display.config(state="normal")
				self.view.button_visualize.config(state="normal")
			tk.messagebox.showinfo("Selection", "Connectome " + str(self.model.name) + " selected.")

	def askDelete(self, event):
		"""
		Asks the user if the selected connectome needs to be deleted.
		:param event: the click event
		:return: None
		"""
		iid = self.view.listConnectomes.identify_row(event.y)
		if iid:
			self.view.listConnectomes.selection_set(iid)
			result = tk.messagebox.askyesno("Suppression", "Do you want to remove this element ?")
			if result:
				self.graphsLoaded.pop(self.view.listConnectomes.selection()[0])
				self.view.listConnectomes.delete(self.view.listConnectomes.selection())
			if len(self.view.listConnectomes.get_children()) == 0:
				self.view.button_display.config(state="disabled")
				self.view.button_visualize.config(state="disabled")
				self.view.button_addinfo.config(state="disabled")
				self.view.button_graph.config(state="disabled")
				self.view.filemenu.entryconfigure(2, state="disabled")
				self.view.filemenu.entryconfigure(3, state="disabled")
				self.model = ConnectomeObject("")
			else:
				self.setSelection()

	def setSelection(self):
		"""
		Sets the selection in the list and update the current connectome as well as the interface.
		:return: None
		"""
		self.view.listConnectomes.selection_set(len(self.graphsLoaded)-1)
		self.model = self.graphsLoaded[self.view.listConnectomes.selection()[0]]
		if networkx.is_empty(self.model.connectomegraph.graph):
			self.view.button_display.config(state="disabled")
			self.view.button_visualize.config(state="disabled")
			self.view.button_addinfo.config(state="disabled")
