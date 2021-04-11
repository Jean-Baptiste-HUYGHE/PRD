from Connectome.ConnectomeObject import ConnectomeObject


"""@package Controller
This module manages the controller part of the windows displayed by the application.
"""


class FormWindowController:
	"""
	Controller class of the form window of the application.
	"""

	def __init__(self, view, parent):
		"""
		Init function for the form controller
		:param view: the window to control
		:param parent: the parent window from which this is created
		"""
		self.parent = parent
		self.view = view

	def createConnectomeObject(self, options):
		"""
		Creates a connectome object from the data input into the form.
		:param options: the list of booleans representing the options
		:return: the ConnectomeObject created
		"""
		model = ConnectomeObject(self.view.name_field.get(), self.view.color.get(), options)
		model.matrixReader.setFileName(self.view.matrixname)
		model.atlasReader.setFileName(self.view.atlasname)
		return model
