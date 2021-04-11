from Comparison.Algorithm import Algorithm
import networkx

"""@package Comparison
This module manages the graph comparison for the connectomes.
"""


class SymmetricDifference(Algorithm):
	"""
	Class for the the symmetric difference algorithm, it creates a graph composed of the edges present in one graph but
	not the other.
	"""

	def __init__(self):
		"""
		Init function for the Ant Colony Optimization
		"""
		super().__init__()

	def compute(self, graphs):
		"""
		Calculation function for symmetric difference
		:return: the resulting graph
		"""
		if len(graphs) != 2:
			return None
		graph1 = graphs[0]
		graph2 = graphs[1]
		newgraph = networkx.symmetric_difference(graph1, graph2)
		return newgraph
