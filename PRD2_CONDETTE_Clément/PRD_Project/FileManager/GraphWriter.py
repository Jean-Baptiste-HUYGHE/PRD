import tempfile

import networkx

from Connectome.ConnectomeGraph import ConnectomeGraph
from FileManager.Writer import Writer

"""@package FileManager
This module manages the reading and writing of files related to the study of connectomes.
"""


class GraphWriter(Writer):
	"""
	Class to write a connectome graph into a file.
	"""

	def __init__(self):
		"""
		Init function for the graph writer
		"""
		super().__init__()

	def writeGraphML(self, graphWritten: ConnectomeGraph):
		"""
		Writes the networkx graph of the ConnectomeGraph into a graphml file
		:param graphWritten: the graph to write
		:return: the filename or an empty string if there is an error
		"""
		try:
			if self.filename.endswith(".graphml"):
				if graphWritten.options['unlinked']:
					copy = graphWritten.graph.copy()
					copy.remove_nodes_from(list(networkx.isolates(copy)))
					networkx.write_graphml(copy, str(self.filename))
				else:
					networkx.write_graphml(graphWritten.graph, str(self.filename))
			else:
				if graphWritten.options['unlinked']:
					copy = graphWritten.graph.copy()
					copy.remove_nodes_from(list(networkx.isolates(copy)))
					networkx.write_graphml(copy, str(self.filename) + ".graphml")
				else:
					networkx.write_graphml(graphWritten.graph, str(self.filename) + ".graphml")
			return self.filename
		except:
			return None

	def writeTempGraphML(self, graphWritten: ConnectomeGraph):
		"""
		Writes the networkx graph of the ConnectomeGraph into a temporary graphml file for previsualisation or graph
		reading operations
		:param graphWritten: the graph to write
		:return: the filename
		"""
		fo = tempfile.NamedTemporaryFile()
		if graphWritten.options['unlinked']:
			copy = graphWritten.graph.copy()
			copy.remove_nodes_from(list(networkx.isolates(copy)))
			networkx.write_graphml(copy, str(fo.name) + ".graphml")
		else:
			networkx.write_graphml(graphWritten.graph, str(fo.name) + ".graphml")
		return fo.name

	def writeGXL(self, graphWritten: ConnectomeGraph):
		"""
		Writes the networkx graph of the ConnectomeGraph into a gxl file
		reading operations
		:param graphWritten: the graph to write
		:return: the filename
		"""
		pass
