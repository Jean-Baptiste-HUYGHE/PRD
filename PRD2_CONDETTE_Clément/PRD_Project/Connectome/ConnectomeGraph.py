import networkx

"""@package Connectome
This module manages the components to manipulate the data about connectomes.
"""


class ConnectomeGraph:
	"""
	Class to represent informations about the graph of the connectome.

	The graph is initialized with a string to represent the color of the edges and a dict of options.

	Options are the following:
		- directed: directed or undirected graph
		- unlinked: removal of isolated nodes
		- weighted: weighted or unweighted edges
		- degree: calculation of the degree of the nodes
		- nodestrength: calculation of the node strength of the nodes (needs a weighted graph)
		- clustering: calculation of the clustering coefficient of the nodes
		- betweenness: calculation of the betweenness centrality of the nodes
		- efficiency: calculation of the global efficiency of the graph (needs an undirected graph)
		- smallworld: calculation fo the smallworld coefficient (needs an undirected and unlinked graph)
	"""

	def __init__(self, color: str = 'grey', options: dict = None):
		"""
		Init function for the connectome graph
		:param color: the color for the visualisation
		:param options: the option to initialize the networkx graph
		"""
		if options is None:
			options = {'directed': False, 'unlinked': False, 'weighted': False,
			           'degree': False, 'nodestrength': False, 'pathlength': False,
			           'clustering': False, 'betweenness': False, 'efficiency': False, 'smallworld': False}
			self.graph = networkx.Graph()
		else:
			if options['directed']:
				self.graph = networkx.DiGraph()
			else:
				self.graph = networkx.Graph()
		self.color = color
		self.options = options
		self.type = "default"
		self.nodecounter = 0

		# Global graph attributes
		self.pathlength = None
		self.smallworldness = None
		self.efficiency = None

	def addNode(self, **kwargs):
		"""
		Add a node to the graph.
		:param kwargs: optional - the parameters of the node
		:return: None
		"""
		self.nodecounter = len(self.graph.nodes) + 1
		number = kwargs.get('number')
		if number is not None:
			self.graph.add_node(int(number))
		else:
			self.graph.add_node(self.nodecounter)

	def addNodeAttributes(self, attributeList, attributeNames):
		"""
		Updates the attributes of the nodes in the graph.
		:param attributeList: the list containing the attributes values
		:param attributeNames: the list containign the attributes names
		:return: None
		"""
		for i in range(len(attributeNames)):
			j = 0
			attributeToNode = dict()
			for node in self.graph.nodes:
				attributeToNode[node] = attributeList[i][j]
				j += 1
			networkx.set_node_attributes(self.graph, attributeToNode, attributeNames[i])

	def addEdge(self, i, j, weight=0):
		"""
		Add an edge between two nodes.
		:param i: the starting node
		:param j: the ending node
		:param weight: the weight of the edge
		:return: None
		"""
		if weight == 0:
			self.graph.add_edge(i, j)
		else:
			self.graph.add_edge(i, j, weight=weight)

	def calculateDegree(self):
		"""
		Calculates the degree of nodes in the graph and adds it as an attribute.
		:return: None
		"""
		# The calculation is the number of edges adjacent to the node
		degree = self.graph.degree
		degree = dict(degree)
		for key in degree:
			degree[key] = round(degree[key], 3)
		networkx.set_node_attributes(self.graph, degree, name='degree')

	def calculateClustering(self):
		"""
		Calculates the clustering coefficient of nodes in the graph and adds it as an attribute.
		:return: None
		"""
		# The clustering coefficient is the ratio between the number of triangle around the node and the
		# maximum number of triangle possible around the node
		# For undirected graph, the number of triangle is 1/2*d*(d-1) with d the degree of the node
		# For directed graph, we consider a triangle only if the directed edges between any three nodes form a cycle
		# The total number of possible triangles is calculated as d_in*d_out-d_ii where d_in and d_out are the in-degree
		# and out-degree of the node and d_ii is the number of connections that cannot form triangles
		clustering = networkx.clustering(self.graph)
		# Cast to float to avoid having different attribute with integer values
		for key in clustering:
			clustering[key] = round(float(clustering[key]), 3)
		networkx.set_node_attributes(self.graph, clustering, name='clustering coefficient')

	def calculatePathLength(self):
		"""
		Calculates the average shortest path length of the graph and adds it as an attribute.
		:return: None
		"""
		# The average shortest path length or characteristic path length is the average all of nodes path_length
		# The path length of a node is the average length of its paths to all other nodes
		copy = self.graph.copy()
		copy.remove_nodes_from(list(networkx.isolates(copy)))
		pathlength = round(networkx.average_shortest_path_length(copy), 3)
		self.pathlength = pathlength
		networkx.set_node_attributes(self.graph, pathlength, name='characteristic path length')

	def calculateStrength(self):
		"""
		Calculates the strength of nodes in the graph and adds it as an attribute.
		:return: None
		"""
		# The strength is the sum of the weights of all the edges adjacent to the node
		strength = dict()
		for node in self.graph.nodes:
			edges = self.graph.edges(node, 'weight')
			weight = 0
			for edge in edges:
				weight += edge[2]
			strength[node] = round(weight, 3)
		networkx.set_node_attributes(self.graph, strength, name='node strength')

	def calculateEfficiency(self):
		"""
		Calculates the global efficiency of the  graph and adds it as an attribute.
		:return: None
		"""
		# The global efficiency of the graph is the average of the global efficiency of all nodes
		# The global efficiency is the average of the inverse shortest path length from a node to all other
		efficiency = round(networkx.global_efficiency(self.graph), 3)
		self.efficiency = efficiency
		networkx.set_node_attributes(self.graph, efficiency, name='global efficiency')

	def calculateBetweennessCentrality(self):
		"""
		Calculates the betweenness centrality of the nodes and adds it as an attribute.
		:return: None
		"""
		# The betweenness centrality is the fraction of shortest path passing through the node
		centrality = networkx.betweenness_centrality(self.graph)
		for key in centrality:
			centrality[key] = round(centrality[key], 3)
		networkx.set_node_attributes(self.graph, centrality, name='betweenness centrality')

	def calculateSmallworldness(self):
		"""
		Calculates the smallworldness coefficent of the graph and adds it as an attribute.
		:return: None
		"""
		# The smallworldness coefficient is a coefficient to determine if a graph can be considered as a small world
		# It is considered a small world if the coefficient is > 1
		# It si calculated as (C/Crnd)/(L/Lrnd) where C and L are the clustering coefficient and the characteristic path
		# length and Crnd and Lrnd are these measures calculated on equivalent random graph
		# This function generates 100 random graphs with the same degree distribution to calculate Crnd and Lrnd, so
		# depending on the size of the graph it might take a long tim to compute
		copy = self.graph.copy()
		copy.remove_nodes_from(list(networkx.isolates(copy)))
		smallworldness = round(networkx.sigma(copy), 3)
		self.smallworldness = smallworldness
		networkx.set_node_attributes(self.graph, smallworldness, name='smallworldness coefficient')

	def calculateInfo(self):
		"""
		Calculates all the information in the graph and adds it as an attribute.
		:return: None
		"""

		if self.options['unlinked']:
			self.graph.remove_nodes_from(list(networkx.isolates(self.graph)))

		if self.options['nodestrength']:
			# In the case of a weighted graph, it shows nodes with a high activity
			self.calculateStrength()

		if self.options['degree']:
			# Shows that every nodes are connected to several other nodes, displaying the level of brain connectivity
			self.calculateDegree()

		if self.options['pathlength']:
			# Calculated on a copy removing the isolated nodes
			self.calculatePathLength()

		if self.options['clustering']:
			# Calculates the clustering coefficient to know if nodes have a tendency to create subgraphs
			# In connectomics, it indicates good brain connections
			self.calculateClustering()

		if self.options['betweenness']:
			# The betweennessCentrality shows if a node is part of the shortest path between two other nodes
			# In connectomics, it shows which nodes are used to communicate between regions
			self.calculateBetweennessCentrality()

		if self.options['efficiency']:
			# The efficiency is a measure of efficient the connections of the graph are
			# In the field of connectomics, it would permit to spot unregular behaviour with bad efficiency
			self.calculateEfficiency()

		# Smallworldness only on non directed graphs
		# Long calculation
		# Interesting to compute because it shows if the graph is more clustered than a random graph with same
		# characteristic path length and degree distribution
		# In connectomics, graphs have a high smallworldness coefficient (>1) because the whole graph is highly connected
		if self.options['smallworld']:
			self.calculateSmallworldness()
