import os
import unittest

import networkx

from Comparison.GraphComparer import GraphComparer
from Comparison.SymmetricDifference import SymmetricDifference
from Connectome.ConnectomeObject import ConnectomeObject
from Visualisation.ConnectomeVisualizer import ConnectomeVisualizer

"""@package Tests
This module manages the testing of the different functions.
"""


class GraphTest(unittest.TestCase):
	"""
	Tests graph creation for different data sets and file types.
	"""

	def test_hospital(self):
		if os.path.exists("hospital.graphml"):
			os.remove("hospital.graphml")
		self.assertFalse(os.path.exists("hospital.graphml"))
		# Smallworld calculation is really long
		options = {'directed': False, 'unlinked': True, 'weighted': True,
		           'degree': True, 'nodestrength': True, 'pathlength': True,
		           'clustering': True, 'betweenness': True, 'efficiency': True, 'smallworld': False}
		connectome = ConnectomeObject("Hospital", "red", options)
		connectome.loadConnectomeAtlasMatrix(matrix="..//Tests_files//MatConn.txt",
											atlas="..//Tests_files//liste_regions_valides.txt")
		connectome.connectomegraph.calculateInfo()
		connectome.graphWriter.setFileName("hospital.graphml")
		connectome.graphWriter.writeGraphML(connectome.connectomegraph)
		self.assertTrue(os.path.exists("hospital.graphml"))

	def test_edge_node(self):
		if os.path.exists("brodmann82.graphml"):
			os.remove("brodmann82.graphml")
		self.assertFalse(os.path.exists("brodmann82.graphml"))
		# Smallworld calculation is really long
		options = {'directed': False, 'unlinked': True, 'weighted': True,
		           'degree': True, 'nodestrength': True, 'pathlength': True,
		           'clustering': True, 'betweenness': True, 'efficiency': True, 'smallworld': False}
		connectome = ConnectomeObject("Brodmann82", "blue", options)
		connectome.loadConnectomeAtlasMatrix(matrix="..//Tests_files//Edge_Brodmann82.edge",
											atlas="..//Tests_files//Node_Brodmann82.node")
		connectome.connectomegraph.calculateInfo()
		connectome.graphWriter.setFileName("brodmann82.graphml")
		connectome.graphWriter.writeGraphML(connectome.connectomegraph)
		self.assertTrue(os.path.exists("brodmann82.graphml"))

	def test_xml(self):
		if os.path.exists("harvardoxford.graphml"):
			os.remove("harvardoxford.graphml")
		self.assertFalse(os.path.exists("harvardoxford.graphml"))
		# Smallworld calculation is really long
		options = {'directed': False, 'unlinked': True, 'weighted': True,
		           'degree': True, 'nodestrength': True, 'pathlength': True,
		           'clustering': True, 'betweenness': True, 'efficiency': True, 'smallworld': False}
		connectome = ConnectomeObject("Harvard-Oxford", "green", options)
		connectome.loadConnectomeAtlasMatrix(matrix="..//Tests_files//harvardoxford_matrix.txt",
											atlas="..//Tests_files//HarvardOxford.xml")
		connectome.connectomegraph.calculateInfo()
		connectome.graphWriter.setFileName("harvardoxford.graphml")
		connectome.graphWriter.writeGraphML(connectome.connectomegraph)
		self.assertTrue(os.path.exists("harvardoxford.graphml"))

	def test_csv(self):
		if os.path.exists("msdl.graphml"):
			os.remove("msdl.graphml")
		self.assertFalse(os.path.exists("msdl.graphml"))
		# Smallworld calculation is really long
		options = {'directed': False, 'unlinked': True, 'weighted': True,
		           'degree': True, 'nodestrength': True, 'pathlength': True,
		           'clustering': True, 'betweenness': True, 'efficiency': True, 'smallworld': False}
		connectome = ConnectomeObject("MSDL", "green", options)
		connectome.loadConnectomeAtlasMatrix(matrix="..//Tests_files//msdl_matrix.txt",
											atlas="..//Tests_files//msdl_rois_labels.csv")
		connectome.connectomegraph.calculateInfo()
		connectome.graphWriter.setFileName("msdl.graphml")
		connectome.graphWriter.writeGraphML(connectome.connectomegraph)
		self.assertTrue(os.path.exists("msdl.graphml"))

	def test_from_graph_brodmann(self):
		self.assertTrue(os.path.exists("brodmann82.graphml"))
		connectome = ConnectomeObject("Brodmann82_from_graphml", "blue")
		connectome.graphReader.setFileName("brodmann82.graphml")
		connectome.loadConnectomeGraph(1)
		connectome.connectomegraph.calculateInfo()
		connectome.graphWriter.setFileName("brodmann82_from_graphml.graphml")
		connectome.graphWriter.writeGraphML(connectome.connectomegraph)
		with open(connectome.graphWriter.filename, newline=None) as file:
			lines_writer = file.readlines()
		with open(connectome.graphReader.filename, newline=None) as file:
			lines_reader = file.readlines()
		self.assertEqual(lines_reader, lines_writer)
		os.remove("brodmann82_from_graphml.graphml")

	def test_from_graph_hospital(self):
		self.assertTrue(os.path.exists("hospital.graphml"))
		connectome = ConnectomeObject("hospital_from_graphml", "blue")
		connectome.graphReader.setFileName("hospital.graphml")
		connectome.loadConnectomeGraph(1)
		connectome.connectomegraph.calculateInfo()
		connectome.graphWriter.setFileName("hospital_from_graphml.graphml")
		connectome.graphWriter.writeGraphML(connectome.connectomegraph)
		with open(connectome.graphWriter.filename, newline=None) as file:
			lines_writer = file.readlines()
		with open(connectome.graphReader.filename, newline=None) as file:
			lines_reader = file.readlines()
		self.assertEqual(lines_reader, lines_writer)
		os.remove("hospital_from_graphml.graphml")

	def test_from_graph_harvardoxford(self):
		self.assertTrue(os.path.exists("harvardoxford.graphml"))
		connectome = ConnectomeObject("harvardoxford_from_graphml", "blue")
		connectome.graphReader.setFileName("harvardoxford.graphml")
		connectome.loadConnectomeGraph(1)
		connectome.connectomegraph.calculateInfo()
		connectome.graphWriter.setFileName("harvardoxford_from_graphml.graphml")
		connectome.graphWriter.writeGraphML(connectome.connectomegraph)
		with open(connectome.graphWriter.filename, newline=None) as file:
			lines_writer = file.readlines()
		with open(connectome.graphReader.filename, newline=None) as file:
			lines_reader = file.readlines()
		self.assertEqual(lines_reader, lines_writer)
		os.remove("harvardoxford_from_graphml.graphml")

	def test_from_graph_msdl(self):
		self.assertTrue(os.path.exists("msdl.graphml"))
		connectome = ConnectomeObject("msdl_from_graphml", "blue")
		connectome.graphReader.setFileName("msdl.graphml")
		connectome.loadConnectomeGraph(1)
		connectome.connectomegraph.calculateInfo()
		connectome.graphWriter.setFileName("msdl_from_graphml.graphml")
		connectome.graphWriter.writeGraphML(connectome.connectomegraph)
		with open(connectome.graphWriter.filename, newline=None) as file:
			lines_writer = file.readlines()
		with open(connectome.graphReader.filename, newline=None) as file:
			lines_reader = file.readlines()
		self.assertEqual(lines_reader, lines_writer)
		os.remove("msdl_from_graphml.graphml")

	def test_calculations(self):
		options = {'directed': False, 'unlinked': True, 'weighted': True,
		           'degree': True, 'nodestrength': True, 'pathlength': True,
		           'clustering': True, 'betweenness': True, 'efficiency': True, 'smallworld': False}
		connectome = ConnectomeObject("", "grey", options)
		connectome.connectomegraph.addNode()
		connectome.connectomegraph.addNode()
		connectome.connectomegraph.addNode()
		connectome.connectomegraph.addNode()
		connectome.connectomegraph.addEdge(1, 2, weight=1)
		connectome.connectomegraph.addEdge(1, 3, weight=1)
		connectome.connectomegraph.addEdge(2, 3, weight=3)
		connectome.connectomegraph.addEdge(1, 4, weight=1)
		connectome.connectomegraph.addEdge(4, 2, weight=2)
		connectome.connectomegraph.calculateInfo()

		self.assertEqual(connectome.connectomegraph.graph.nodes().get(1)['degree'], 3)
		self.assertEqual(connectome.connectomegraph.graph.nodes().get(1)['node strength'], 3)
		self.assertEqual(connectome.connectomegraph.graph.nodes().get(1)['clustering coefficient'], 0.667)
		self.assertEqual(connectome.connectomegraph.graph.nodes().get(1)['betweenness centrality'], 0.167)

		self.assertEqual(connectome.connectomegraph.graph.nodes().get(2)['degree'], 3)
		self.assertEqual(connectome.connectomegraph.graph.nodes().get(2)['node strength'], 6)
		self.assertEqual(connectome.connectomegraph.graph.nodes().get(2)['clustering coefficient'], 0.667)
		self.assertEqual(connectome.connectomegraph.graph.nodes().get(2)['betweenness centrality'], 0.167)

		self.assertEqual(connectome.connectomegraph.graph.nodes().get(3)['degree'], 2)
		self.assertEqual(connectome.connectomegraph.graph.nodes().get(3)['node strength'], 4)
		self.assertEqual(connectome.connectomegraph.graph.nodes().get(3)['clustering coefficient'], 1.0)
		self.assertEqual(connectome.connectomegraph.graph.nodes().get(3)['betweenness centrality'], 0.0)

		self.assertEqual(connectome.connectomegraph.graph.nodes().get(4)['degree'], 2)
		self.assertEqual(connectome.connectomegraph.graph.nodes().get(4)['node strength'], 3)
		self.assertEqual(connectome.connectomegraph.graph.nodes().get(4)['clustering coefficient'], 1.0)
		self.assertEqual(connectome.connectomegraph.graph.nodes().get(4)['betweenness centrality'], 0.0)

		self.assertEqual(connectome.connectomegraph.pathlength, 1.167)
		self.assertEqual(connectome.connectomegraph.efficiency, 0.917)

	def testReloadGraph(self):
		connectome = ConnectomeObject("msdl_from_graphml", "blue")
		connectome.graphReader.setFileName("msdl.graphml")
		connectome.loadConnectomeGraph(1)
		self.assertFalse(networkx.is_empty(connectome.connectomegraph.graph))
		graphBefore = connectome.connectomegraph.graph.copy()
		self.assertEqual(connectome.connectomegraph.efficiency, None)
		options = {'directed': False, 'unlinked': False, 'weighted': False,
		           'degree': False, 'nodestrength': False, 'pathlength': False,
		           'clustering': False, 'betweenness': False, 'efficiency': True, 'smallworld': False}
		connectome.reloadGraph(options)
		self.assertFalse(networkx.is_empty(connectome.connectomegraph.graph))
		self.assertEqual(graphBefore.nodes, connectome.connectomegraph.graph.nodes)
		self.assertEqual(graphBefore.edges, connectome.connectomegraph.graph.edges)
		self.assertNotEqual(connectome.connectomegraph.efficiency, None)

	def testSubGraph(self):
		self.assertTrue(os.path.exists("brodmann82.graphml"))
		connectome = ConnectomeObject("Brodmann82_from_graphml", "blue")
		connectome.graphReader.setFileName("brodmann82.graphml")
		connectome.loadConnectomeGraph(1)
		connectome.connectomegraph.calculateInfo()

		connectome_left = connectome.createSubGraph("left")
		connectome_right = connectome.createSubGraph("right")

		connectome_whole = ConnectomeObject("Brodmann82_left_plus_right", "blue")
		connectome_whole.connectomegraph.graph = networkx.union(connectome_left, connectome_right)

		visualizer = ConnectomeVisualizer()
		visualizer.visualizeConnectomeGraph(connectome)
		visualizer.visualizeConnectomeGraph(connectome_whole)

		self.assertIsNotNone(connectome_left)
		self.assertIsNotNone(connectome_right)
		self.assertIsNotNone(connectome_whole.connectomegraph.graph)
		self.assertIsNotNone(connectome.connectomegraph.graph)

	def testSymmetricDifference(self):
		connectome1 = ConnectomeObject("100206", "grey")
		connectome2 = ConnectomeObject("100307", "grey")
		connectome1.graphReader.setFileName("..//Tests_files//comparison//humans//100206_repeated10_scale33.graphml")
		connectome2.graphReader.setFileName("..//Tests_files//comparison//humans//100307_repeated10_scale33.graphml")
		connectome1.loadConnectomeGraph(1)
		connectome2.loadConnectomeGraph(1)
		self.assertNotEqual(connectome1.connectomegraph.graph.graph, {})
		self.assertNotEqual(connectome2.connectomegraph.graph.graph, {})
		sym = SymmetricDifference()
		comparer = GraphComparer(sym)
		result = comparer.compareGraphs([connectome1.connectomegraph.graph, connectome2.connectomegraph.graph])
		self.assertIsNotNone(result)
		connectomeResult = ConnectomeObject("100206 x 100307", "grey")
		connectomeResult.connectomegraph.graph = result
		visualizer = ConnectomeVisualizer()
		output = visualizer.visualizeConnectomeGraph(connectome1)
		self.assertTrue(output)
		output = visualizer.visualizeConnectomeGraph(connectome2)
		self.assertTrue(output)
		output = visualizer.visualizeConnectomeGraph(connectomeResult)
		self.assertTrue(output)


