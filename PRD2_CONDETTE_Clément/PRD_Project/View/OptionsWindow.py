import tkinter.tix as Tix
from tkinter import *

from Controller import MainWindowController

"""@package View
This module manages the different windows of the application.
"""


class OptionsWindow(Toplevel):
	"""
    Class for the window to select graph options.
    """

	def __init__(self, parent, **kwargs):
		"""
        Init function for the option window
        :param parent: the parent window
        :param kwargs: the arguments for the tkinter.Toplevel superclass
        """
		super().__init__(**kwargs)
		self.parent = parent
		self.resizable(0, 0)
		self.title("Options selection")

		self.directed = IntVar()
		self.unlinked = IntVar()
		self.weighted = IntVar()
		self.degree = IntVar()
		self.nodestrength = IntVar()
		self.pathlength = IntVar()
		self.clustering = IntVar()
		self.betweenness = IntVar()
		self.efficiency = IntVar()
		self.smallworld = IntVar()

		self.main_frame = Frame(self, width=200, height=400)
		self.main_frame.grid(row=0, column=0, padx=10, pady=5)
		self.option_label = Label(self.main_frame, text="Options", font=("Courier", 18))
		self.option_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='news')

		self.directed_label = Label(self.main_frame, text="Directed graph:")
		self.directed_label.grid(row=2, column=0, padx=5, pady=5, sticky='news')
		self.directed_check = Checkbutton(self.main_frame, variable=self.directed,
		                                  command=lambda f=1: self.checkConditionDirected())
		self.directed_check.grid(row=2, column=1, padx=5, pady=5, sticky='news')
		self.unlinked_label = Label(self.main_frame, text="Remove isolated nodes:")
		self.unlinked_label.grid(row=3, column=0, padx=5, pady=5, sticky='news')
		self.unlinked_check = Checkbutton(self.main_frame, variable=self.unlinked,
		                                  command=lambda f=1: self.checkConditionUnlinked())
		self.unlinked_check.grid(row=3, column=1, padx=5, pady=5, sticky='news')
		self.weight_label = Label(self.main_frame, text="Weighted edges:")
		self.weight_label.grid(row=4, column=0, padx=5, pady=5, sticky='news')
		self.weight_check = Checkbutton(self.main_frame, variable=self.weighted,
		                                command=lambda f=1: self.checkConditionWeighted())
		self.weight_check.grid(row=4, column=1, padx=5, pady=5, sticky='news')
		self.degree_label = Label(self.main_frame, text="Nodes degree:")
		self.degree_label.grid(row=5, column=0, padx=5, pady=5, sticky='news')
		self.degree_check = Checkbutton(self.main_frame, variable=self.degree)
		self.degree_check.grid(row=5, column=1, padx=5, pady=5, sticky='news')
		self.nodestrength_label = Label(self.main_frame, text="Nodes strength:")
		self.nodestrength_label.grid(row=6, column=0, padx=5, pady=5, sticky='news')
		self.nodestrength_check = Checkbutton(self.main_frame, variable=self.nodestrength,
		                                      command=lambda f=1: self.checkConditionNodeStrength())
		self.nodestrength_check.grid(row=6, column=1, padx=5, pady=5, sticky='news')
		self.pathlength_label = Label(self.main_frame, text="Characteristic path length:")
		self.pathlength_label.grid(row=7, column=0, padx=5, pady=5, sticky='news')
		self.pathlength_check = Checkbutton(self.main_frame, variable=self.pathlength)
		self.pathlength_check.grid(row=7, column=1, padx=5, pady=5, sticky='news')
		self.clustering_label = Label(self.main_frame, text="Clustering coefficient:")
		self.clustering_label.grid(row=8, column=0, padx=5, pady=5, sticky='news')
		self.clustering_check = Checkbutton(self.main_frame, variable=self.clustering)
		self.clustering_check.grid(row=8, column=1, padx=5, pady=5, sticky='news')
		self.betweenness_label = Label(self.main_frame, text="Betweenness centrality:")
		self.betweenness_label.grid(row=9, column=0, padx=5, pady=5, sticky='news')
		self.betweenness_check = Checkbutton(self.main_frame, variable=self.betweenness)
		self.betweenness_check.grid(row=9, column=1, padx=5, pady=5, sticky='news')
		self.efficiency_label = Label(self.main_frame, text="Global efficiency:")
		self.efficiency_label.grid(row=10, column=0, padx=5, pady=5, sticky='news')
		self.efficiency_check = Checkbutton(self.main_frame, variable=self.efficiency,
		                                    command=lambda f=1: self.checkConditionEfficiency())
		self.efficiency_check.grid(row=10, column=1, padx=5, pady=5, sticky='news')
		self.smallworldness_label = Label(self.main_frame, text="Smallworldness coefficient:")
		self.smallworldness_label.grid(row=11, column=0, padx=5, pady=5, sticky='news')
		self.smallworldness_check = Checkbutton(self.main_frame, variable=self.smallworld,
		                                        command=lambda f=1: self.checkConditionSmallworld())
		self.smallworldness_check.grid(row=11, column=1, padx=5, pady=5, sticky='news')

		self.button_OK = Button(self.main_frame, text="OK", fg="black", command=lambda f=1: self.validate())
		self.button_OK.grid(row=12, column=0, padx=5, pady=5, sticky='news')
		self.button_cancel = Button(self.main_frame, text="Cancel", fg="black", command=lambda f=1: self.destroy())
		self.button_cancel.grid(row=12, column=1, padx=5, pady=5, sticky='news')

		directedBalloon = Tix.Balloon()
		directedBalloon.bind_widget(self.directed_label, msg="Toggles the graph as directed or undirected.")

		unlinkedBalloon = Tix.Balloon()
		unlinkedBalloon.bind_widget(self.unlinked_label, msg="Ignores the isolated nodes (no edges).")

		weightedBalloon = Tix.Balloon()
		weightedBalloon.bind_widget(self.weight_label, msg="Toggles the graph as weighted or unweighted.")

		degreeBalloon = Tix.Balloon()
		degreeBalloon.bind_widget(self.degree_label, msg="Toggles the calculation of the degree of the nodes.")

		strengthBalloon = Tix.Balloon()
		strengthBalloon.bind_widget(self.nodestrength_label,
		                            msg="Toggles the calculation of the strength of the nodes.")

		pathlengthBalloon = Tix.Balloon()
		pathlengthBalloon.bind_widget(self.pathlength_label,
		                              msg="Toggles the calculation of the characteristic path length.")

		clusteringBalloon = Tix.Balloon()
		clusteringBalloon.bind_widget(self.clustering_label,
		                              msg="Toggles the calculation of the clustering coefficient.")

		centralityBalloon = Tix.Balloon()
		centralityBalloon.bind_widget(self.betweenness_label,
		                              msg="Toggles the calculation of the betweenness centrality.")

		efficiencyBalloon = Tix.Balloon()
		efficiencyBalloon.bind_widget(self.efficiency_label, msg="Toggles the calculation of the global efficiency.\n"
		                                                         "The graph must be undirected")

		smallworldnessBalloon = Tix.Balloon()
		smallworldnessBalloon.bind_widget(self.smallworldness_label, msg="Enables the calculation of "
		                                                                 "the smallworldness coefficient.(This operation might take a long time).\n The graph must be undirected.")

		if isinstance(self.parent, MainWindowController.MainWindowController):
			if self.parent.model.connectomegraph.options['directed']:
				self.directed.set(1)
			if self.parent.model.connectomegraph.options['weighted']:
				self.weighted.set(1)
			if self.parent.model.connectomegraph.options['unlinked']:
				self.unlinked.set(1)
			if self.parent.model.connectomegraph.options['degree']:
				self.degree.set(1)
			if self.parent.model.connectomegraph.options['nodestrength']:
				self.nodestrength.set(1)
			if self.parent.model.connectomegraph.options['pathlength']:
				self.pathlength.set(1)
			if self.parent.model.connectomegraph.options['clustering']:
				self.clustering.set(1)
			if self.parent.model.connectomegraph.options['betweenness']:
				self.betweenness.set(1)
			if self.parent.model.connectomegraph.options['efficiency']:
				self.efficiency.set(1)
			if self.parent.model.connectomegraph.options['smallworld']:
				self.smallworld.set(1)
			if self.parent.model.matrixReader.filename is None:
				self.directed_check.config(state="disabled")
				self.weight_check.config(state="disabled")
				if self.directed.get():
					self.smallworldness_check.config(state="disabled")
					self.efficiency_check.config(state="disabled")
				if not self.weighted.get():
					self.nodestrength_check.config(state="disabled")

		self.protocol("WM_DELETE_WINDOW", self.destroy)
		self.config()
		self.mainloop()

	def validate(self):
		"""
		Returns the options of the connectome to the parent window.
		:return: None
		"""
		options = {'directed': self.directed.get(), 'unlinked': self.unlinked.get(), 'weighted': self.weighted.get(),
		           'degree': self.degree.get(), 'nodestrength': self.nodestrength.get(),
		           'pathlength': self.pathlength.get(), 'clustering': self.clustering.get(),
		           'betweenness': self.betweenness.get(), 'efficiency': self.efficiency.get(),
		           'smallworld': self.smallworld.get()}
		if isinstance(self.parent, MainWindowController.MainWindowController):
			self.parent.model.connectomegraph.options = options
			self.parent.checkAndUpdate(self.smallworld.get())
		else:
			self.parent.options = options
			self.parent.createObject()
		self.destroy()

	def checkConditionUnlinked(self):
		"""
		Checks the condition of the unlinked option
		:return: None
		"""
		if self.unlinked.get() == 0:
			if self.smallworld.get() == 1:
				self.smallworld.set(0)

	def checkConditionDirected(self):
		"""
		Checks the condition of the directed option
		:return: None
		"""
		if self.directed.get() == 1:
			if self.smallworld.get() == 1:
				self.smallworld.set(0)
			if self.efficiency.get() == 1:
				self.efficiency.set(0)

	def checkConditionEfficiency(self):
		"""
		Checks the condition of the efficiency option
		:return: None
		"""
		if self.efficiency.get() == 1:
			if self.directed.get() == 1:
				self.directed.set(0)

	def checkConditionSmallworld(self):
		"""
		Checks the condition of the smallworldness option
		:return: None
		"""
		if self.smallworld.get() == 1:
			if self.directed.get() == 1:
				self.directed.set(0)
			if self.unlinked.get() == 0:
				self.unlinked.set(1)

	def checkConditionNodeStrength(self):
		"""
		Checks the conditions of the node strength option
		:return: None
		"""
		if self.nodestrength.get() == 1:
			if self.weighted.get() == 0:
				self.weighted.set(1)

	def checkConditionWeighted(self):
		"""
		Checks the conditions of the weighted option
		:return: None
		"""
		if self.weighted.get() == 0:
			if self.nodestrength.get() == 1:
				self.nodestrength.set(0)
