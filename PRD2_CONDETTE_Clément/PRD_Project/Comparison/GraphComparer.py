"""@package Comparison
This module manages the graph comparison for the connectomes.
"""


class GraphComparer:
	"""
	Class comparing several graphs using an comparison algorithm.
	"""

	def __init__(self, algorithm):
		"""
		Init function for the GraphComparer
		"""
		self.algorithm = algorithm

	def compareGraphs(self, graphs):
		"""
		Function for the comparison of graphs
		:return: the result of the comparison
		"""
		return self.algorithm.compute(graphs)
