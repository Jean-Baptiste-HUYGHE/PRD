"""@package FileManager
This module manages the reading and writing of files related to the study of connectomes.
"""


class Writer:
	"""
	Class to write a file.
	"""

	def __init__(self):
		"""
		Init function for the writer
		"""
		self.filename = None

	def setFileName(self, filename):
		"""
		Sets the filename.
		:param filename: the filename to be set
		:return: None
		"""
		self.filename = filename

	def write(self, content, **kwargs):
		"""
		Function opening a file and writing content into it
		:param content: the content to write
		:return: None
		"""
		mode = kwargs.get('mode')
		if mode == ('w', 'a', 'w+', 'a+'):
			with open(self.filename, newline=None, mode=mode) as file:
				file.writelines(content)
		else:
			with open(self.filename, newline=None, mode='w+') as file:
				file.writelines(content)
