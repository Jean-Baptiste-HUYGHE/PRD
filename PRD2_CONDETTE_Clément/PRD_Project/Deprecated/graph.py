import networkx

"""
Classe gérant les graphes de l'application. 
La classe Graphe possède un attribut graph qui représente le graphe networkx ainsi que des options pour l'affichage et
l'écriture dans un fichier.
"""


class Graph:

	"""
	Fonction d'initialisation de la classe. Prend en paramètre:
	- graph: un graphe networkx
	- color: string pour définir la couleur des sommets si on désire la choisir
	- unlinked: boolean pour définir si on utilise les sommets sans arêtes
	- degree: boolean pour définir si on veut calculer le degré des sommets
	- path: boolean pour définir si on veut calculer la longueur des chemins moyenne
	- cluster: boolean pour définir si on veut calculer le coefficient de clustering
	- smallworld: string pour définir si on veut calculer le degré des sommets
	"""
	def __init__(self, graph: networkx.Graph, color: str, unlinked: bool, degree: bool, path: bool, cluster: bool, smallworld: bool):
		self.graph = graph
		self.color = color
		self.unlinked = unlinked
		self.degree = degree
		self.path = path
		self.cluster = cluster
		self.smallworld = smallworld
		self.smallworldness = None
		self.clustering = None
		self.pathlength = None
		self.nodecounter = 0

	"""
	Ajoute un sommet au graphe en fonction des options passées en argument.
	"""
	def addNode(self, **kwargs):
		self.nodecounter = len(self.graph.nodes)+1
		number = kwargs.get('number')
		if number is not None:
			self.graph.add_node(int(number))
		else:
			self.graph.add_node(self.nodecounter)


	"""
	Ajoute à tout les nodes du graphes les valeurs pour un attribut donné
	"""
	def addNodeAttributes(self, attributeList, attributeNames):
		for i in range(len(attributeNames)):
			j = 0
			attributeToNode = dict()
			for node in self.graph.nodes:
				attributeToNode[node] = attributeList[i][j]
				j += 1
			networkx.set_node_attributes(self.graph, attributeToNode, attributeNames[i])


	"""
	Ajoute une arête entre deux sommets donnés
	"""
	def addEdge(self, i, j, weight):
		self.graph.add_edge(i, j, weight=weight)

	"""
	Exporte le graphe au format graphml
	"""
	def writeAsGraphml(self, fileName):
		if fileName.endswith(".graphml"):
			if self.unlinked:
				copy = self.graph.copy()
				copy.remove_nodes_from(list(networkx.isolates(copy)))
				networkx.write_graphml(copy, str(fileName))
			else:
				networkx.write_graphml(self.graph, str(fileName))
		else:
			if self.unlinked:
				copy = self.graph.copy()
				copy.remove_nodes_from(list(networkx.isolates(copy)))
				networkx.write_graphml(copy, str(fileName) + ".graphml")
			else:
				networkx.write_graphml(self.graph, str(fileName) + ".graphml")

	"""
	Calcule le degré des sommets
	"""
	def calculateDegree(self, graph):
		degree = graph.degree
		degree = dict(degree)
		networkx.set_node_attributes(graph, degree, name='degree')

	"""
	Calcule le clustering des sommets
	"""
	def calculateClustering(self, graph):
		clustering = networkx.clustering(graph)
		# On caste les valeurs en float pour ne pas avoir plusieurs attributs différents
		for key in clustering:
			clustering[key] = float(clustering[key])

		networkx.set_node_attributes(graph, clustering, name='clustering coefficient')
		self.clustering = networkx.average_clustering(graph)

	"""
	Calcule des charactéristiques supplémentaires comme le coefficient de clustering, la longueur de chemin 
	caractéristique et la small-worldness
	"""
	def calculateInfo(self):
		# On crée une copie du graphe qui exclut les sommets isolés pour effectuer les calculs
		copy = self.graph.copy()
		copy.remove_nodes_from(list(networkx.isolates(copy)))

		if self.degree:
			self.calculateDegree(self.graph)

		# Doit être calculé sur la copie pour ignorer les sommets isolés
		if self.path:
			self.pathlength = networkx.average_shortest_path_length(copy)

		if self.cluster:
			self.calculateClustering(self.graph)

		# Le calcul de smallworldness ne fonctionne pas sur des graphes dirigés
		# Ce calcul est très long
		if self.smallworld:
			if not copy.is_directed():
				self.smallworldness = networkx.sigma(copy)
