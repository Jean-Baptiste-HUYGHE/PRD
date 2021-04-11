import os

import networkx
import networkx as nx
import plotly as py
import plotly.graph_objs as go
import webview
# from nilearn import datasets, surface

from Connectome import ConnectomeGraph
from Connectome.ConnectomeObject import ConnectomeObject
from Visualisation.GraphVisualizer import GraphVisualizer

"""@package Visualisation
This module manages the objects to visualize connectomes in a 3D environment.
"""


class ConnectomeVisualizer(GraphVisualizer):
	"""
	Class to visualize the connectome as a 3D network based on the networkx graph of the ConnectomeObject's ConnectomeGraph
	"""

	def __init__(self):
		"""
        Init function for the connectome vizualiser
        """
		super().__init__()

	def visualizeConnectomeGraph(self, connectome: ConnectomeObject, volume: bool = False, viztype="default"):
		"""
		Visualize the connectome as a 3D network from a ConnectomeObject.
		:param viztype: type of vizualisation for the graph
		:param connectome: the connectome to display
		:param volume: boolean for the usage of a brainvolume
		:return: boolean to designate if the connectome is displayed
		"""

		# if volume:
		# 	# Fetch the brain mesh from freesurfer to get the coordinates for a plotly 3D mesh plotting
		# 	mesh = datasets.fetch_surf_fsaverage()
		# 	mesh_coord = []
		# 	# We only want the pial left and right hemisphere which is the non-inflated surface of the hemispheres
		# 	for hemi in ['pial_left', 'pial_right']:
		# 		mesh_coord.append(surface.load_surf_mesh(mesh[hemi]))
		#
		# 	# Arrays for each type of value
		# 	mesh_x = []
		# 	mesh_y = []
		# 	mesh_z = []
		# 	mesh_i = []
		# 	mesh_j = []
		# 	mesh_k = []
		#
		# 	# Fills the coordinates for the x, y, z coordinates of the vertices for the brain mesh
		# 	for i in range(len(mesh_coord)):
		# 		for j in range(len(mesh_coord[i][0])):
		# 			mesh_x.append(mesh_coord[i][0][j][0])
		# 			mesh_y.append(mesh_coord[i][0][j][0])
		# 			mesh_z.append(mesh_coord[i][0][j][0])
		#
		# 	# Fills the coordinates of the i,j,k vertices for the triangles
		# 	for i in range(len(mesh_coord)):
		# 		for j in range(len(mesh_coord[i][1])):
		# 			mesh_i.append(mesh_coord[i][1][j][0])
		# 			mesh_j.append(mesh_coord[i][1][j][1])
		# 			mesh_k.append(mesh_coord[i][1][j][2])

		G = connectome.connectomegraph.graph
		color = self.selectColor(connectome.connectomegraph)

		# Get a node from the nodes of the graph to read its attributes
		for value in G.nodes():
			node = value
			break

		# Initialize a list of attributes for the legend
		attributes = G.nodes().get(node).keys()

		x = 0
		y = 0
		z = 0
		# Looks for coordinates attributes by looking for similar attribute names
		for att in attributes:
			if 'x' in att:
				x = str(att)
			if x and 'y' in att:
				if x.replace('x', 'y') == att:
					y = str(att)
			if x and 'z' in att:
				if x.replace('x', 'z') == att:
					z = str(att)
			if x and y and z:
				break

		# Initialize the labels with the attributes read from the attribute list
		if x != 0 and y != 0 and z != 0:
			# Get the x coordinates of the nodes in the graph to determine the hemisphere
			Xn = list(nx.get_node_attributes(G, x).values())
			# Cast to float in case the coordinates are saved as strings
			Xn = [float(n) for n in Xn]

			if viztype != "default":
				separator = (max(Xn)+min(Xn))/2
				totalNodes = G.copy().nodes()
				for node in totalNodes:
					xval = float(totalNodes.get(node)[x])
					if xval > separator and viztype == "right":
						G.remove_node(node)
					if xval < separator and viztype == "left":
						G.remove_node(node)
				if viztype == "unlinked":
					G.remove_nodes_from(list(networkx.isolates(G)))

			Nodes = G.nodes()
			Edges = G.edges()
			N = len(Nodes)

			# Get the coordinates of the nodes in the graph
			Xn = list(nx.get_node_attributes(G, x).values())
			Yn = list(nx.get_node_attributes(G, y).values())
			Zn = list(nx.get_node_attributes(G, z).values())

			for value in G.nodes():
				node = value
				break

			if 'id' in Nodes[node]:
				labels = list(nx.get_node_attributes(G, 'id').values())
			else:
				labels = [str(k) for k in range(N)]

			index = 0
			legend = list()
			# Format the legend as HTML to write with plotly
			for label in labels:
				line = ""
				line = line + str("<br><b>index</b>: " + label + "<br>")
				for att in attributes:
					attlist = list(nx.get_node_attributes(G, att).values())
					line = line + str("<br><b>" + att + "</b>: " + str(attlist[index]) + "<br>")
				index += 1
				legend.append(line)

			Xe = []
			Ye = []
			Ze = []
			# Get the start and end coordinates of the edges of the graph
			for e in Edges:
				Xe += [Nodes.get(e[0])[x], Nodes.get(e[1])[x], None]
				Ye += [Nodes.get(e[0])[y], Nodes.get(e[1])[y], None]
				Ze += [Nodes.get(e[0])[z], Nodes.get(e[1])[z], None]

			# Edges of the graph
			trace1 = go.Scatter3d(
				# X, Y, Z coordinates for the edges
				x=Xe,
				y=Ye,
				z=Ze,
				mode='lines',
				line=dict(color=color, width=1),
				hoverinfo='none'
			)

			# Nodes of the graph
			trace2 = go.Scatter3d(
				# X, Y, Z coordinates for the nodes
				x=Xn,
				y=Yn,
				z=Zn,
				mode='markers',
				# Type of representation for the nodes
				marker=dict(symbol='circle',
				            size=6,
				            colorscale='Viridis',
				            line=dict(color='rgb(50,50,50)', width=0.5)
				            ),
				text=legend,
				hoverinfo='text'
			)

			# Axis variable for the layout
			axis = dict(showbackground=False,
			            showline=False,
			            zeroline=False,
			            showgrid=False,
			            showticklabels=False,
			            title=''
			            )

			# Layout of the plot
			layout = go.Layout(
				title="3D Representation of " + connectome.name,
				width=1000,
				height=1000,
				showlegend=False,
				scene=dict(
					xaxis=dict(axis),
					yaxis=dict(axis),
					zaxis=dict(axis),
				),
				margin=dict(
					t=100
				),
				hovermode='closest')

			# if volume:
			# 	# Maps a mesh shaped like a brain
			# 	vol = go.Mesh3d(
			# 		x=mesh_x,
			# 		y=mesh_y,
			# 		z=mesh_z,
			# 		# Greyscale
			# 		colorscale=[[0, 'grey'],
			# 		            [1, 'grey']],
			# 		showscale=False,
			# 		# Intensity of each vertex, which will be interpolated and color-coded
			# 		intensity=np.linspace(0, 1, 12, endpoint=True),
			# 		intensitymode='cell',
			# 		# Low opacity to be see-through
			# 		opacity=0.2,
			# 		# No hovering info so we can hover the inside scatter plot
			# 		hoverinfo='none',
			# 		# i, j and k give the vertices of triangles
			# 		i=mesh_i,
			# 		j=mesh_j,
			# 		k=mesh_k,
			# 	)

			# Draw the figure with the data intialized above
			if volume:
				data = [trace1, trace2]
			# data = [trace1, trace2, vol]
			else:
				data = [trace1, trace2]
			fig = go.Figure(data=data, layout=layout)

			# We use the offline version to remove the need for an internet connection
			# Write the data in an html file
			py.offline.plot(fig, filename=connectome.name + ".html", auto_open=False)
			htmlfile = open(connectome.name + ".html", 'r')

			# Creates a window emulating a navigator and display the HTML code generated by plotly
			window = webview.create_window(connectome.name, html=htmlfile.read()
			                               , width=1000, height=800)
			webview.start(None, window)
			while not window.closed:
				continue
			# Upon closing the window, close and delete the HTML file created
			htmlfile.close()
			os.remove(connectome.name + ".html")
			return True
		else:
			# If 3D coordinates can't be found, the graph is not displayed
			print("No coordinates, graph cannot be visualized in a 3D environment")
			return False

	def visualizeConnectomeGraphFile(self, filename):
		"""
		Visualize the connectome as a 3D network from a graph file
		:param filename: the name of the file to read
		:return: None
		"""
		pass

	def selectColor(self, connectomegraph: ConnectomeGraph):
		"""
		Returns a string corresponding with the color of the graph or a default grey color
		:param connectomegraph: the graph which color needs to be read
		:return: the color string
		"""
		if connectomegraph.color == "grey":
			color = 'rgb(125,125,125)'
		elif connectomegraph.color == "red":
			color = 'rgb(255,0,0)'
		elif connectomegraph.color == "blue":
			color = 'rgb(0,0,255)'
		elif connectomegraph.color == "green":
			color = 'rgb(0,255,0)'
		elif connectomegraph.color == "yellow":
			color = 'rgb(240,255,50)'
		elif connectomegraph.color == "black":
			color = 'rgb(0,0,0)'
		else:
			color = 'rgb(125,125,125)'
		return color
