from FileManager.Writer import Writer

"""@package FileManager
This module manages the reading and writing of files related to the study of connectomes.
"""


class AtlasWriter(Writer):
	"""
	Class to write a connectome graph into a file.
	"""

	def __init__(self):
		"""
		Init function for the atlas writer
		"""
		super().__init__()

	def writeXML(self):
		"""
		Write the atlas of the connectome in an xml file
		:return: None
		"""
		pass

	def writeCSV(self):
		"""
		Write the atlas of the connectome in a csv file
		:return: None
		"""
		pass

	def writeNODE(self):
		"""
		Write the atlas of the connectome in a node file
		:return: None
		"""
		pass
