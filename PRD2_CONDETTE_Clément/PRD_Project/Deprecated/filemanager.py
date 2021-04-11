import csv
import re
import xml.dom.minidom

import networkx as nx

from Deprecated.graph import Graph

"""
Classe permettant de construire un graphe à partir de données de connectome.
Pour fonctionner, la class prend à minima un fichier contenant la matrice de connectivité et un fichier contenant
l'atlas utilisé pour construire le connectome.
"""


class FileManager:
	"""
	Fonction d'initialisation de la classe.
	Des options peuvent être passées en paramètres:
	- unlinked: boolean pour définir si on affiche les sommets sans arêtes
	- color: string pour définir la couleur des sommets si on désire la choisir
	- weighted: boolean pour définir si les arêtes ont un poids
	- directed: boolean pour définir si le graphe est orienté ou non.
	Un graphe orienté ne peut pas être un graphe 'small-world'
	"""
	def __init__(self, *args, **kwargs):
		self.matConn = None
		self.atlas = None
		self.unlinked = None
		self.color = None
		self.directed = True
		self.weighted = True
		self.currGraph = None
		options = None
		if len(kwargs) == 0:
			noOption = True
		else:
			noOption = False
			options = kwargs

		if noOption:
			self.initializeNoOption(args)
		else:
			self.initializeOptions(args, options)

	"""
	Initialise les paramètres si il n'y a pas d'options sélectionnées.
	"""
	def initializeNoOption(self, args):
		if len(args) == 2:
			self.atlas = args[0]
			self.matConn = args[1]
		else:
			raise ValueError("Paramètres incorrects")

	"""
	Initialise les paramètres en fonction des options sélectionnées
	"""
	def initializeOptions(self, args, options):
		self.initializeNoOption(args)
		for key in options:
			if key == 'unlinked':
				self.unlinked = options[key]
			if key == 'color':
				self.color = options[key]
			if key == 'weighted':
				self.weighted = options[key]
			if key == 'directed':
				self.directed = options[key]

	"""
	Créer un graphe networkx et l'initialise à partir des données présentes dans l'atlas et la matrice de connectivité
	"""
	def generateGraph(self, degree, path, cluster, smallworld):
		if not self.directed:
			self.currGraph = Graph(nx.Graph(), self.color, self.unlinked, degree, path, cluster, smallworld)
		else:
			self.currGraph = Graph(nx.DiGraph(), self.color, self.unlinked, degree, path, cluster, smallworld)
		self.readAtlas()
		self.readMatrix(self.weighted)
		self.currGraph.calculateInfo()

	"""
	#OLD
	Lecture de l'atlas pour initialiser les sommets du graphe.
	"""
	def readAtlas_old(self):
		with open(self.atlas, newline=None) as regions:
			if self.atlas.endswith(('.csv', '.txt')):
				fields = self.checkFields()
				region_reader = csv.reader(regions, delimiter=fields[0])
				number = None
				label = None
				posX = None
				posY = None
				posZ = None
				autre = None
				for region in region_reader:
					index = 1
					for field in region:
						if fields[index] == 'x':
							posX = field
						if fields[index] == 'y':
							posY = field
						if fields[index] == 'z':
							posZ = field
						if fields[index] == 'label':
							label = field
						if fields[index] == 'autre':
							autre = field
						index += 1
					self.currGraph.addNode(number=number, label=label, x=posX, y=posY, z=posZ, autre=autre)

			elif self.atlas.endswith('.xml'):
				region_reader = xml.dom.minidom.parse(regions)
				nodes = region_reader.getElementsByTagName("label")
				for node in nodes:
					number = None
					label = None
					posX = None
					posY = None
					posZ = None
					if 'index' in node.attrib:
						number = node.getAttribute("index")
					if node.firstChild:
						label = node.firstChild.nodeValue
					if 'x' in node.attrib:
						posX = node.getAttribute("x")
					if 'y' in node.attrib:
						posY = node.getAttribute("y")
					if 'z' in node.attrib:
						posZ = node.getAttribute("z")
					self.currGraph.addNode(number=number, label=label, x=posX, y=posY, z=posZ)

			elif self.atlas.endswith('.node'):
				region_reader = csv.reader(regions, delimiter='\t')
				number = 1
				for region in region_reader:
					self.currGraph.addNode(number=number, x=region[0], y=region[1], z=region[2], color=region[3],
												degree=region[4], label=region[5])
					number += 1

	"""
	Lecture de l'atlas pour initialiser les sommets du graphe.
	"""
	def readAtlas(self):
		# Ouvre l'atlas du manager
		with open(self.atlas, newline=None) as regions:
			# Cas où on a un fichier csv ou un txt au format csv
			if self.atlas.endswith(('.csv', '.txt')):
				fields = self.checkFields()
				region_reader = csv.reader(regions, delimiter=fields[0])

				# Cas où il existe un header, on l'ignore
				sample = regions.read(10000)
				regions.seek(0)
				if csv.Sniffer().has_header(sample):
					next(region_reader)

				# On enlève le champ index
				index = 0
				indexed = False
				# On cherche si il y a un champ index du sommet
				attributeName = fields[1:]
				for i in range(len(attributeName)):
					if attributeName[i] == 'index':
						indexed = True
						break
					index += 1
				attributeValues = [[] for i in range(len(attributeName))]
				node_number = 0
				for region in region_reader:
					for i in range(len(attributeName)):
						attributeValues[i].append(region[i])
					if indexed:
						self.currGraph.addNode(number=region[index])
					else:
						node_number += 1
						self.currGraph.addNode(number=node_number)
				if indexed:
					attributeValues.pop(0)
					attributeName.pop(index)
				self.currGraph.addNodeAttributes(attributeValues, attributeName)

			elif self.atlas.endswith('.xml'):
				attributeName = ['label', 'x', 'y', 'z']
				attributeValues = [[] for i in range(4)]
				region_reader = xml.dom.minidom.parse(regions)
				nodes = region_reader.getElementsByTagName("label")
				for node in nodes:
					attributeValues[0].append(node.firstChild.nodeValue)
					attributeValues[1].append(node.getAttribute("x"))
					attributeValues[2].append(node.getAttribute("y"))
					attributeValues[3].append(node.getAttribute("z"))
					self.currGraph.addNode(number=node.getAttribute("index"))
				self.currGraph.addNodeAttributes(attributeValues, attributeName)

			elif self.atlas.endswith('.node'):
				region_reader = csv.reader(regions, delimiter='\t')
				#regions.seek(0)
				attributeName = ['x', 'y', 'z', 'color', 'degree', 'label']
				attributeValues = [[] for i in range(6)]
				node_number = 0
				for region in region_reader:
					# Permet de passer un éventuel header
					if re.search('[a-zA-Z]', region[0]):
						continue
					attributeValues[0].append(region[0])
					attributeValues[1].append(region[1])
					attributeValues[2].append(region[2])
					attributeValues[3].append(region[3])
					attributeValues[4].append(region[4])
					attributeValues[5].append(region[5])
					node_number += 1
					self.currGraph.addNode(number=node_number)
				self.currGraph.addNodeAttributes(attributeValues, attributeName)


	"""
	Lecture de la matrice de connectivité
	On peut décider de lire la matrice de manière non-pondérée
	"""
	def readMatrix(self, weighted):
		with open(self.matConn, newline=None) as connect:
			i = 0
			for conn in connect:
				j = 0
				nb = self.currGraph.graph.number_of_nodes()
				nodes = list(self.currGraph.graph.nodes().keys())
				if conn.__contains__(','):
					split = conn.split(',')
				else:
					split = conn.split()
				for edge in split:
					if float(edge) != 0 and i < nb:
						if weighted:
							self.currGraph.addEdge(nodes[i], nodes[j], float(edge))
						else:
							self.currGraph.addEdge(nodes[i], nodes[j], 1)
					j += 1
				i += 1

	"""
	Fonction qui lit un fichier txt ou csv et retourne une liste contenant la signification des champs et le délimiteur
	"""
	def checkFields(self):
		with open(self.atlas, newline=None) as regions:
			# Lecture de la première ligne pour vérifier s'il existe un header
			sample = regions.read(10000)
			dialect = csv.Sniffer().sniff(sample)

			# Cas où il y a un header à lire
			if csv.Sniffer().has_header(sample):
				regions.seek(0)
				header = next(csv.reader(regions, delimiter=dialect.delimiter))
				fields_csv = [str(dialect.delimiter)]
				for field in header:
					fields_csv.append(str(field))
			else:
				regions.seek(0)
				row = next(csv.reader(regions, delimiter=dialect.delimiter))
				fields_csv = ['' for x in range(len(row) + 1)]
				fields_csv[0] = dialect.delimiter
				# Booléens pour définir si on a trouvé ces paramètres
				coord = False
				number = False
				labeled = False
				index = 0
				while index < len(row):
					case = 0
					try:
						if float(row[index]):
							case = 1
							if float(row[index + 1]):
								if float(row[index + 2]):
									case = 2
									if float(row[index + 3]):
										case = 3
					except (ValueError, IndexError):
						pass
					if case != 0 and coord:
						case = 1
					if case == 0:
						if not labeled:
							fields_csv[index+1] = 'label'
							labeled = True
						else:
							fields_csv[index + 1] = 'valeur'
					elif case == 1:
						if not number:
							fields_csv[index+1] = 'index'
							number = True
						else:
							fields_csv[index + 1] = 'number'
					elif case == 2:
						coord = True
						fields_csv[index + 1] = 'x'
						fields_csv[index + 2] = 'y'
						fields_csv[index + 3] = 'z'
						index += 2
					else:
						coord = True
						number = True
						fields_csv[index + 1] = 'index'
						fields_csv[index + 2] = 'x'
						fields_csv[index + 3] = 'y'
						fields_csv[index + 4] = 'z'
						index += 3
					index += 1
			return fields_csv
