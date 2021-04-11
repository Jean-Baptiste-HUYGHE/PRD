from FileManager.Writer import Writer

"""@package FileManager
This module manages the reading and writing of files related to the study of connectomes.
"""


class MatrixWriter(Writer):
	"""
	Class to write a connectome connectivity matrix into a file.
	"""

	def __init__(self):
		"""
		Init function for the matrix writer
		"""
		super().__init__()

	def writeMatrix(self):
		"""
		Write the matrix of the connectome in a txt file
		:return: None
		"""
		pass

	def writeEDGE(self):
		"""
		Write the matrix of the connectome in an edge file
		:return: None
		"""
		pass
