from FileManager.BrainReader import BrainReader

"""@package Connectome
This module manages the components to manipulate the data about connectomes.
"""


class BrainVolume:
	"""
	Class for the brain volume file of a connectome. Most of the time using a niftii file for medical imaging.
	"""

	def __init__(self, color):
		"""
		Init function for the brain volume
		:param color: color of the brain volume modelisation
		"""
		self.reader = None
		self.color = color

	def setReader(self, filename):
		"""
		Set the brain reader for the volume
		:param filename: The name of the niftii file to read
		:return: None
		"""
		self.reader = BrainReader()
		self.reader.filename = filename



