from Connectome import ConnectomeGraph
from FileManager.Reader import Reader

"""@package FileManager
This module manages the reading and writing of files related to the study of connectomes.
"""


class MatrixReader(Reader):
	"""
	Class to read a connectivity matrix file.
	"""

	def __init__(self):
		"""
		Init function for the matrix reader
		"""
		super().__init__()

	def readMatrix(self, graph: ConnectomeGraph, weighted):
		"""
		Function reading a connectivity matrix to create edges in the graph.
		:param graph: the graph to modify
		:param weighted: boolean to determine if edges are weighted
		:return: None
		"""
		with open(self.filename, newline=None) as connect:
			i = 0
			for conn in connect:
				j = 0
				nb = graph.graph.number_of_nodes()
				nodes = list(graph.graph.nodes().keys())
				if conn.__contains__(','):
					split = conn.split(',')
				else:
					split = conn.split()
				for edge in split:
					if float(edge) != 0 and i < nb:
						if weighted:
							graph.addEdge(nodes[i], nodes[j], float(edge))
						else:
							graph.addEdge(nodes[i], nodes[j], 0)
					j += 1
				i += 1
