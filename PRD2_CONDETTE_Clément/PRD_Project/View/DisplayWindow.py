import tkinter as tk

"""@package View
This module manages the different windows of the application.
"""


class DisplayWindow(tk.Toplevel):
    """
    Class for the window displaying the information on the graph.
    """

    def __init__(self, model, **kwargs):
        """
        Init function for the display window
        :param model: the ConnectomeObject to display
        :param kwargs: the arguments for the tkinter.Toplevel superclass
        """
        super().__init__(**kwargs)
        self.title("Informations on graph " + model.name)
        self.resizable(0, 0)
        self.geometry("+300+300")
        self.labelName = tk.Label(self, text="Name: " + str(model.name))
        self.labelName.grid(row=0, column=0, sticky="news")

        if model.connectomegraph.options['directed']:
            self.labelDirected = tk.Label(self, text="Directed: Yes")
            self.labelDirected.grid(row=1, column=0, sticky="news")
        else:
            self.labelDirected = tk.Label(self, text="Directed: No")
            self.labelDirected.grid(row=1, column=0, sticky="news")

        if model.connectomegraph.options['unlinked']:
            self.labelUnlinked = tk.Label(self, text="Isolated nodes: No")
            self.labelUnlinked.grid(row=2, column=0, sticky="news")
        else:
            self.labelUnlinked = tk.Label(self, text="Isolated nodes: Yes")
            self.labelUnlinked.grid(row=2, column=0, sticky="news")

        if model.connectomegraph.options['weighted']:
            self.labelWeighted = tk.Label(self, text="Weighted: Yes")
            self.labelWeighted.grid(row=3, column=0, sticky="news")
        else:
            self.labelWeighted = tk.Label(self, text="Weighted: No")
            self.labelWeighted.grid(row=3, column=0, sticky="news")

        row = 4

        if model.connectomegraph.options['pathlength']:
            self.labelPathlength = tk.Label(self,
                                            text="Characteristic path length: " + str(model.connectomegraph.pathlength))
            self.labelPathlength.grid(row=row, column=0, sticky="news")
            row += 1
        if model.connectomegraph.options['efficiency']:
            self.labelEfficiency = tk.Label(self,
                                            text="Global efficiency: " + str(model.connectomegraph.efficiency))
            self.labelEfficiency.grid(row=row, column=0, sticky="news")
            row += 1
        if model.connectomegraph.options['smallworld']:
            self.labelSmallworld = tk.Label(self, text="Smallworldness coefficient: "
                                                       + str(model.connectomegraph.smallworldness))
            self.labelSmallworld.grid(row=row, column=0, sticky="news")
            row += 1

        self.button1 = tk.Button(self, text="OK", command=lambda f=1: self.ok())
        self.button1.grid(row=row, column=0, sticky="news")

        self.lift()
        self.config()
        self.mainloop()

    def ok(self):
        """
        Function for the "OK" button of the application.
        :return: None
        """
        self.destroy()
