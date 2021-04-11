import csv
import re
import xml.dom.minidom

from Connectome import ConnectomeGraph
from FileManager.Reader import Reader

"""@package FileManager
This module manages the reading and writing of files related to the study of connectomes.
"""


class AtlasReader(Reader):
	"""
	Class to read a brain atlas file.
	"""

	def __init__(self):
		"""
		Init function for the atlas reader
		"""
		super().__init__()

	def readAtlas(self, graph: ConnectomeGraph):
		"""
		Read an atlas file in a .csv, .txt, .xml or .node file to add nodes to a graph.
		:param graph: the graph to update with the found nodes
		:return: None
		"""
		work = False
		with open(self.filename, newline=None) as regions:
			# Case of a csv or txt file
			work = True
			if self.filename.endswith(('.csv', '.txt')):
				fields = self.checkFields()
				region_reader = csv.reader(regions, delimiter=fields[0])

				# Ignore header if found
				sample = regions.read(10000)
				regions.seek(0)
				if csv.Sniffer().has_header(sample):
					next(region_reader)

				index = 0
				indexed = False
				# Look for an index field and tag it if found
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
						graph.addNode(number=region[index])
					else:
						node_number += 1
						graph.addNode(number=node_number)
				if indexed:
					attributeValues.pop(0)
					attributeName.pop(index)
				graph.addNodeAttributes(attributeValues, attributeName)

			# Case of an xml file
			elif self.filename.endswith('.xml'):
				attributeName = ['label', 'x', 'y', 'z']
				attributeValues = [[] for i in range(4)]
				region_reader = xml.dom.minidom.parse(regions)
				nodes = region_reader.getElementsByTagName("label")
				for node in nodes:
					attributeValues[0].append(node.firstChild.nodeValue)
					attributeValues[1].append(node.getAttribute("x"))
					attributeValues[2].append(node.getAttribute("y"))
					attributeValues[3].append(node.getAttribute("z"))
					graph.addNode(number=node.getAttribute("index"))
				graph.addNodeAttributes(attributeValues, attributeName)

			# Case of a node file
			elif self.filename.endswith('.node'):
				region_reader = csv.reader(regions, delimiter='\t')
				attributeName = ['x', 'y', 'z', 'color', 'degree', 'label']
				attributeValues = [[] for i in range(6)]
				node_number = 0
				for region in region_reader:
					# Skip header if found
					if re.search('[a-zA-Z]', region[0]):
						continue
					attributeValues[0].append(region[0])
					attributeValues[1].append(region[1])
					attributeValues[2].append(region[2])
					attributeValues[3].append(region[3])
					attributeValues[4].append(region[4])
					attributeValues[5].append(region[5])
					node_number += 1
					graph.addNode(number=node_number)
				graph.addNodeAttributes(attributeValues, attributeName)
		return work

	def checkFields(self):
		"""
		Read the atlas to look for a header or to test fields and estimate the values.
		:return: list of fields in the atlas
		"""
		with open(self.filename, newline=None) as regions:
			# Search header
			sample = regions.read(10000)
			dialect = csv.Sniffer().sniff(sample)

			# Case with header
			if csv.Sniffer().has_header(sample):
				regions.seek(0)
				header = next(csv.reader(regions, delimiter=dialect.delimiter))
				fields_csv = [str(dialect.delimiter)]
				for field in header:
					fields_csv.append(str(field))
			# Case with no header
			else:
				regions.seek(0)
				row = next(csv.reader(regions, delimiter=dialect.delimiter))
				fields_csv = ['' for x in range(len(row) + 1)]
				fields_csv[0] = dialect.delimiter
				# Booleans to tag parameters found
				coord = False
				number = False
				labeled = False
				index = 0
				# Tests each field
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
