import networkx

from Connectome.ConnectomeGraph import ConnectomeGraph
from FileManager.Reader import Reader

"""@package FileManager
This module manages the reading and writing of files related to the study of connectomes.
"""


class GraphReader(Reader):
	"""
	Class to read a brain atlas file.
	"""

	def __init__(self):
		"""
		Init function for the graph reader
		"""
		super().__init__()

	def readGraphML(self):
		"""
		Reads a graphML file and initialize a connectome graph object with the corresponding information
		:return: the ConnectomeGraph object
		"""
		graph = ConnectomeGraph()
		graph_read = networkx.read_graphml(self.filename)
		graph.graph = graph_read
		if graph.graph.is_directed():
			graph.options['directed'] = True
		graph.color = 'grey'
		if len(list(networkx.isolates(graph_read))) == 0:
			graph.options['unlinked'] = True
		if networkx.get_edge_attributes(graph_read, 'weight'):
			graph.options['weighted'] = True
		if networkx.get_node_attributes(graph_read, 'degree'):
			graph.options['degree'] = True
		if networkx.get_node_attributes(graph_read, 'smallworldness coefficient'):
			graph.options['smallworld'] = True
		return graph


	def readGXL(self):
		"""
		Reads a GXL file and initialize a connectome graph object with the corresponding information
		:return: the ConnectomeGraph object
		"""
		pass
