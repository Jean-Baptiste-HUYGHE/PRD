from FileManager.Reader import Reader

"""@package FileManager
This module manages the reading and writing of files related to the study of connectomes.
"""


class BrainReader(Reader):
	"""
	Class to read a brain atlas file.
	"""

	def __init__(self):
		"""
		Init function for the brain reader
		"""
		super().__init__()

	def readNiftii(self):
		"""
		Read a Niftii file containing a brain volume.
		:return: None
		"""
		pass
