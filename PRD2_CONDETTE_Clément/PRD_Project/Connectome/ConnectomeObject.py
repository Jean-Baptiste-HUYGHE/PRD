import networkx

from Connectome.ConnectomeGraph import ConnectomeGraph
from FileManager.AtlasReader import AtlasReader
from FileManager.GraphReader import GraphReader
from FileManager.GraphWriter import GraphWriter
from FileManager.MatrixReader import MatrixReader

"""@package Connectome
This module manages the components to manipulate the data about connectomes.
"""


class ConnectomeObject:
	"""
	Class for connectome objects used to initialize the connectome with different parameters.
	Contains the Connectomegraph attribute that represents the networkx graph.
	The reader and writer attributes are used to manipulate files for the creation and writing of graphs.
	"""

	def __init__(self, name, color: str = 'grey', options=None):
		"""
		Init function for the connectome object
		:param name: the name of the connectome
		:param color: the color for the visualisation
		:param options: the option to initialize the networkx graph
		"""
		self.name = name
		self.volume = None
		if not options:
			self.options = {'directed': False, 'unlinked': False, 'weighted': False,
			           'degree': False, 'nodestrength': False, 'pathlength': False,
			           'clustering': False, 'betweenness': False, 'efficiency': False, 'smallworld': False}
			self.connectomegraph = ConnectomeGraph(color, self.options)
		else:
			self.connectomegraph = ConnectomeGraph(color, options)
		self.matrixReader = MatrixReader()
		self.atlasReader = AtlasReader()
		self.graphReader = GraphReader()
		self.graphWriter = GraphWriter()

	def loadConnectomeGraph(self, typeFile):
		"""
		Loads a connectome from a graph file
		:param typeFile: integer representing the type of file to read
		:return: None
		"""
		try:
			if typeFile == 1:
				self.connectomegraph = self.graphReader.readGraphML()
			elif typeFile == 2:
				self.connectomegraph = self.graphReader.readGXL()
			return True
		except Exception:
			return False

	def loadConnectomeAtlasMatrix(self, option="default", **kwargs):
		"""
		Loads a connectome from a connectivity matrix and an atlas
		:param option:
		:param kwargs: parameters to set the name of the files if needed
		:return: None
		"""
		try:
			for key, value in kwargs.items():
				if key == 'matrix':
					self.matrixReader.setFileName(value)
				if key == 'atlas':
					self.atlasReader.setFileName(value)

			self.atlasReader.readAtlas(self.connectomegraph)
			self.matrixReader.readMatrix(self.connectomegraph, self.connectomegraph.options['weighted'])
			if option == "left" or option == "right":
				graph = self.createSubGraph(option)
				if graph is None:
					return False
				else:
					self.connectomegraph.graph = graph
			if self.connectomegraph.options['unlinked']:
				self.connectomegraph.graph.remove_nodes_from(
					list(networkx.isolates(self.connectomegraph.graph)))
			self.connectomegraph.calculateInfo()
			return True
		except NameError:
			return False

	def setBrainVolume(self, volume):
		"""
		Sets a brian volume for the visualization
		:param volume: the brain volume file used in the visualization
		:return: None
		"""
		self.volume = volume

	def setFilenames(self, matrixName, atlasName, graphName):
		"""
		Sets all the filenames for the readers
		:param matrixName: the name of the matrix file
		:param atlasName: the name of the atlas file
		:param graphName: the name of the graph file
		:return:
		"""
		self.matrixReader.filename = matrixName
		self.atlasReader.filename = atlasName
		self.graphReader.filename = graphName

	def reloadGraph(self, options):
		"""
		Reload the connectome with a new set of options.
		:param options: The new options
		:return: None
		"""
		if self.graphReader.filename.endswith(".graphml"):
			self.loadConnectomeGraph(1)
		elif self.graphReader.filename.endswith(".gxl"):
			self.loadConnectomeGraph(2)
		else:
			self.loadConnectomeAtlasMatrix(self.connectomegraph.type)
		self.connectomegraph.options = options
		self.connectomegraph.calculateInfo()

	def createSubGraph(self, option):
		"""
		Create a subgraph of the current graph corresponding to the selected option.
		:param option: The type of subgraph wanted, currently right or left hemisphere
		:return: The subgraph created
		"""
		subgraph = self.connectomegraph.graph.copy()

		# Get a node from the nodes of the graph to read its attributes
		for value in self.connectomegraph.graph.nodes():
			node = value
			break

		# Initialize a list of attributes for the legend
		attributes = self.connectomegraph.graph.nodes().get(node).keys()
		x = None
		for att in attributes:
			if 'x' in att:
				x = str(att)

		if x is None:
			print("Error, can't find coordinates.")
			return None
		Xn = list(networkx.get_node_attributes(self.connectomegraph.graph, x).values())
		Xn = [float(n) for n in Xn]

		separator = (max(Xn) + min(Xn)) / 2
		totalNodes = self.connectomegraph.graph.copy().nodes()
		for node in totalNodes:
			xval = float(totalNodes.get(node)[x])
			if xval > separator and option == "right":
				subgraph.remove_node(node)
			if xval < separator and option == "left":
				subgraph.remove_node(node)
		self.connectomegraph.type = option
		return subgraph

	def loadSubGraph(self, option):
		"""
		Loads and set the subgraph created from the option passed as parameter
		:param option: the type of subgraph wanted, right now only left and right hemisphere
		:return: a boolean to confirm the subgraph creation
		"""
		subgraph = self.createSubGraph(option)
		if subgraph is not None:
			self.connectomegraph.graph = subgraph
			return True
		else:
			return False
