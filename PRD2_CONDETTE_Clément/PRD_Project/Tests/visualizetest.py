import unittest

from Connectome.ConnectomeObject import ConnectomeObject
from Visualisation.ConnectomeVisualizer import ConnectomeVisualizer

"""@package Tests
This module manages the testing of the different functions.
"""


class VisualizeTest(unittest.TestCase):
	"""
	Tests graph visualization from different data sets and with different configuration
	"""

	def test_brodmann82view(self):
		options = {'directed': False, 'unlinked': True, 'weighted': True,
		           'degree': True, 'nodestrength': True, 'pathlength': True,
		           'clustering': True, 'betweenness': True, 'efficiency': True, 'smallworld': False}
		connectome = ConnectomeObject("Brodmann82", "grey", options)
		connectome.loadConnectomeAtlasMatrix(matrix="..//Tests_files//Edge_Brodmann82.edge",
		                                     atlas="..//Tests_files//Node_Brodmann82.node")
		visualizer = ConnectomeVisualizer()
		result = visualizer.visualizeConnectomeGraph(connectome)
		self.assertTrue(result)

	def test_hospitalview(self):
		options = {'directed': False, 'unlinked': True, 'weighted': True,
		           'degree': True, 'nodestrength': True, 'pathlength': True,
		           'clustering': True, 'betweenness': True, 'efficiency': True, 'smallworld': False}
		connectome = ConnectomeObject("Hospital", "red", options)
		connectome.loadConnectomeAtlasMatrix(matrix="..//Tests_files/MatConn.txt",
		                                     atlas="..//Tests_files//liste_regions_valides.txt")
		visualizer = ConnectomeVisualizer()
		result = visualizer.visualizeConnectomeGraph(connectome)
		self.assertFalse(result)

	def test_msdlview(self):
		options = {'directed': False, 'unlinked': True, 'weighted': True,
		           'degree': True, 'nodestrength': True, 'pathlength': True,
		           'clustering': True, 'betweenness': True, 'efficiency': True, 'smallworld': False}
		connectome = ConnectomeObject("MSDL", "blue", options)
		connectome.loadConnectomeAtlasMatrix(matrix="..//Tests_files//msdl_matrix.txt",
		                                     atlas="..//Tests_files//msdl_rois_labels.csv")
		visualizer = ConnectomeVisualizer()
		result = visualizer.visualizeConnectomeGraph(connectome)
		self.assertTrue(result)

	def test_harvardoxfordview(self):
		options = {'directed': False, 'unlinked': False, 'weighted': False,
		           'degree': True, 'nodestrength': False, 'pathlength': True,
		           'clustering': True, 'betweenness': True, 'efficiency': True, 'smallworld': False}
		connectome = ConnectomeObject("Harvard-Oxford", options=options)
		connectome.graphReader.setFileName("harvardoxford.graphml")
		connectome.loadConnectomeGraph(1)
		visualizer = ConnectomeVisualizer()
		connectome.connectomegraph.color = "green"
		result = visualizer.visualizeConnectomeGraph(connectome)
		self.assertTrue(result)

	def test_visualizeLeft(self):
		options = {'directed': False, 'unlinked': True, 'weighted': True,
		           'degree': True, 'nodestrength': True, 'pathlength': True,
		           'clustering': True, 'betweenness': True, 'efficiency': True, 'smallworld': False}
		connectome = ConnectomeObject("Brodmann82 - Left", "grey", options)
		connectome.loadConnectomeAtlasMatrix("left", matrix="..//Tests_files//Edge_Brodmann82.edge",
		                                     atlas="..//Tests_files//Node_Brodmann82.node")
		visualizer = ConnectomeVisualizer()
		result = visualizer.visualizeConnectomeGraph(connectome)
		self.assertTrue(result)

	def test_visualizeRight(self):
		options = {'directed': False, 'unlinked': True, 'weighted': True,
		           'degree': True, 'nodestrength': True, 'pathlength': True,
		           'clustering': True, 'betweenness': True, 'efficiency': True, 'smallworld': False}
		connectome = ConnectomeObject("Brodmann82 - Right", "grey", options)
		connectome.loadConnectomeAtlasMatrix("right", matrix="..//Tests_files//Edge_Brodmann82.edge",
		                                     atlas="..//Tests_files//Node_Brodmann82.node")
		visualizer = ConnectomeVisualizer()
		result = visualizer.visualizeConnectomeGraph(connectome)
		self.assertTrue(result)
