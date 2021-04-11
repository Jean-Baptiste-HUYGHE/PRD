"""@package Visualisation
This module manages the objects to visualize connectomes in a 3D environment.
"""


class GraphVisualizer:
	"""
	Class to vizualise a networkx 3D network
	"""

	def __init__(self):
		"""
		Init function for the graph vizualiser
		"""
		self.graphFile = None

	def setGraphFile(self, filename):
		"""
		Sets the filename.
		:param filename: the filename to be set
		:return: None
		"""
		self.graphFile = filename

	def visualizeGraph(self, graph):
		"""
		Displays a networkx graph with 3D coordinates.
		:param graph: the graph to display
		:return: None
		"""
		pass
