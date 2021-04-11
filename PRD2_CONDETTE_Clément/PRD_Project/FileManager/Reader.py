"""@package FileManager
This module manages the reading and writing of files related to the study of connectomes.
"""


class Reader:
	"""
	Class to read a file.
	"""

	def __init__(self):
		"""
		Init function for the reader
		"""
		self.filename = None

	def setFileName(self, filename):
		"""
		Sets the filename.
		:param filename: the filename to be set
		:return: None
		"""
		self.filename = filename

	def read(self):
		"""
		Function opening a file and returning its content
		:return: list of lines in the file
		"""
		with open(self.filename, newline=None) as file:
			lines = file.readlines()
		return lines
