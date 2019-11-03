from topology import Topology
import networkx as nx 
import matplotlib.pyplot as plt
import copy

class Plotter:

	pos = None

	def find_sinks(self, topology):
		potential_sinks = topology.components
		for connection in topology.connections:
			if connection[0] in potential_sinks:
				potential_sinks.remove(connection[0])
		return potential_sinks	

	components_in_layers = []

	def align_layers(self, node_positions, topology, prev_layer, cnt):
		next_layer = []
		for connection in topology.connections:
			if connection[1] in prev_layer and connection[0] not in self.components_in_layers:
				next_layer.append(connection[0])

		if len(next_layer) == 0:
			return

		i = 0
		for node in next_layer:
			node_positions[node.u_name][0] = i
			node_positions[node.u_name][1] = cnt+1
			i = i+1

		self.components_in_layers = next_layer + self.components_in_layers
		self.align_layers(node_positions, topology, next_layer, cnt+1)


	def align_nodes(self, node_positions, topology):
		# find a component with only outgoing connections
		# -> bottom layer
		sinks = self.find_sinks(topology)

		# base layer = 1
		i = 0
		for sink in sinks:
			#print("sink " + str(sink.u_name))
			node_positions[sink.u_name][0] = i
			node_positions[sink.u_name][1] = 1
			i = i+1

		self.components_in_layers = self.components_in_layers + sinks
		self.align_layers(node_positions, topology, sinks, 1)

	def plot(self, topology):
		components_in_layers = []
		pos = None
		G = nx.OrderedDiGraph()
		node_id_to_type = {}
		node_id_to_name = {}
		#print(topology)

		top = copy.deepcopy(topology)

		for component in top.components:
			G.add_nodes_from([component.u_name])
			node_id_to_type[component.u_name] = 'mediumseagreen'
			node_id_to_name[component.u_name] = component.component_type.u_name
			#print("adding node " + component.u_name)

		for connection in top.connections:
			#print("adding connection " + connection[0].u_name + " " + connection[1].u_name)
			if connection[0].u_name in node_id_to_name and connection[1].u_name in node_id_to_name:
				G.add_edge(connection[0].u_name, connection[1].u_name)

		self.pos = nx.planar_layout(G) # initial position for all nodes

		self.align_nodes(self.pos, top)

		color_map = []
		for node in G:
			color_map.append(node_id_to_type[node])

		nx.draw_networkx_labels(G,self.pos,node_id_to_name,font_size=15, node_color='b')

		nx.draw(G,self.pos, node_size=1000,node_color=color_map, arrowsize=30)