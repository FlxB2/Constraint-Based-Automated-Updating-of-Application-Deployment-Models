class Topology:
	def __init__(self):
		self.components = []
		self.connections = []

	def add_connection(self, conn):
		a,b = conn
		self.connections.append((a,b))

	def remove_connection(self, a):
		self.connections.remove(a)

	def add_component(self, a):
		self.components.append(a)

	def remove_component(self, a):
		self.components.remove(a)

	def change_component(self, a, b):
		self.remove_component(a)
		self.add_component(b)

	def __str__(self):
		result = "Topology content: \n"
		result = result + "COMPONENTS: \n"
		for component in self.components:
			result = result + str(component) + "\n"
		result = result + "CONNECTIONS: \n"
		for connection in self.connections: 
			result = result + connection[0].u_name + ":" + connection[1].u_name + "\n"
		return result


class Component:
	def __init__(self, u_name, component_type):
		self.u_name = u_name
		self.component_type = component_type

	def __str__(self):
		return "{Component " + self.u_name + " of type " + str(self.component_type) + "}"

class Component_Type:
	def __init__(self, u_name, parent, caps, reqs):
		self.u_name = u_name
		self.parent = parent
		self.caps = caps
		self.reqs = reqs

	def __str__(self):
		return "{Component type \"" + str(self.u_name) + "\" parent \"" + str(self.parent) + "\" cap \"" + str(self.caps) + "\" req \"" + str(self.reqs) + "\"}"