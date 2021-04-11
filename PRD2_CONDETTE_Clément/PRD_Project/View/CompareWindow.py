import tkinter as tk

"""@package View
This module manages the different windows of the application.
"""


class CompareWindow(tk.Toplevel):
    """
    Class for the graph comparison window.
    """

    def __init__(self, **kwargs):
        """
        Init function for the graph comparison window
        :param kwargs: the arguments for the tkinter.Toplevel superclass
        """
        super().__init__(**kwargs)
