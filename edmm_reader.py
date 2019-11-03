import yaml
import uuid
from topology import *
import re
from pathlib import Path


# reads edmm files
# and converts them into local self.topology / type representation

class EDMM_Reader:

	# prevents cyclic dependencies
	imported_list = []

	resolved_types = {}

	topology = Topology()

	def read_types(self, src):
		yaml_content = yaml.safe_load(open(str(src), "r"))
		base_path = src.parents[0]
		#print("working in dir " + str(base_path))

		if "imports" in yaml_content:
			for imported in yaml_content["imports"]:
				print("resolving import " + str(str(base_path)+"/"+imported))
				if imported not in self.imported_list:
					yaml_content.update(yaml.safe_load(open(str(base_path)+imported, "r")))
					self.imported_list.append(imported)

		# look at all component_types
		if "component_types" in yaml_content:
			for component_type_name in yaml_content["component_types"]:
				self.resolve_component_type(yaml_content, component_type_name)

	# resolve types recursively, this is not ideal but does the job
	def resolve_component_type(self, yaml_content, component_type_name):
		component_type = yaml_content["component_types"][component_type_name]

		caps = None
		req = None
		parent = None

		if not component_type_name in self.resolved_types:
			if "capabilities" in component_type:
				caps = caps_to_string_list(component_type["capabilities"])
			if "requirements" in component_type:
				req = reqs_to_string_list(component_type["requirements"])
			parent_name = component_type["extends"]
			if not parent_name in self.resolved_types:
				if not parent_name is None:
					self.resolve_component_type(yaml_content, parent_name)	

			if not parent_name is None:
				parent = self.resolved_types[parent_name]
			resolved_component_type = Component_Type(component_type_name, parent, caps, req)
			self.resolved_types[component_type_name] = resolved_component_type
			#print("added: " + component_type_name + " \n" + str(resolved_component_type))

	def read_components(self, src):
		yaml_content = yaml.safe_load(open(str(src), "r"))
		base_path = src.parents[0]
		#print("working in dir " + str(base_path))

		if "imports" in yaml_content:
			for imported in yaml_content["imports"]:
				print("resolving import " + str(str(base_path)+"/"+imported))
				self.read_types(Path(base_path,imported))
		if "components" in yaml_content:
			for component in yaml_content["components"]:
				name = component
				#component_type = yaml_content["components"][component]["type"]
				component_type = self.resolved_types[yaml_content["components"][component]["type"]]
				if component_type == None:
					print("component " + name + " does not have a type.. ignoring")
				else:
					tmp_component = Component(name, component_type)
					self.topology.add_component(tmp_component)

		else:
			print("no components found in " + src)

	def inherent_reqs_caps_of_parents(self, component_types):
		for key in component_types:
			if component_types[key].caps != None:
				component_types[key].caps = component_types[key].caps + self.get_caps_of_parent(component_types[key])
			if component_types[key].reqs != None:
				component_types[key].reqs = component_types[key].reqs + self.get_reqs_of_parent(component_types[key])
		return component_types

	def get_caps_of_parent(self, component_type):
		if component_type.parent == None or component_type.parent.caps == None:
			return []

		result = []
		for cap in component_type.parent.caps:
			result.append(cap)

		result = result + self.get_caps_of_parent(component_type.parent)
		return result

	def get_reqs_of_parent(self, component_type):
		if component_type.parent == None or component_type.parent.reqs == None:
			return []

		result = []
		for req in component_type.parent.reqs:
			result.append(req)

		result = result + self.get_reqs_of_parent(component_type.parent)
		return result

	def quick_hack(self, name):
		name = name
		for component in self.topology.components:
			if name == component.u_name:
				return component

	def read_connections(self, src):
		yaml_content = yaml.safe_load(open(str(src), "r"))

		if "components" in yaml_content:
			for component_type_name in yaml_content["components"]:
				yaml_object = yaml_content["components"][component_type_name]
				if "relations" in yaml_object:
					component_object = self.quick_hack(component_type_name)
					#print(str(yaml_object) + " " + str(component_object))
					relations = yaml_object["relations"]
					for relation in relations:
						for key in relation:
							component_object_connected = self.quick_hack(relation[key])
							if component_object_connected is not None and component_object is not None:
								self.topology.add_connection((component_object, component_object_connected))

	# returns tuple of self.topology and self.resolved_types
	def read_edmm(self, src):
		print("reading edmm " + str(src))
		self.read_components(src)
		self.resolved_types = self.inherent_reqs_caps_of_parents(self.resolved_types)
		self.read_connections(src)
		print(self.topology)
		return self.topology, self.resolved_types

def u_string_from_key_value(key, value):
		return value

def caps_to_string_list(yaml):
	result = []
	for cap in yaml:
		# capabilities are lists
		key = list(cap.keys())[0]
		value = cap[key]
		result.append(u_string_from_key_value(key,value))
	return result

def reqs_to_string_list(yaml):
	result = []
	for req in yaml:
		# req are lists
		# relation type is of no interest -> ignore it
		key = list(req.keys())[0]
		print(req)
		print(key)
		print(req[key])
		value = req[key]["capability"]
		result.append(u_string_from_key_value(key,value))
	return result