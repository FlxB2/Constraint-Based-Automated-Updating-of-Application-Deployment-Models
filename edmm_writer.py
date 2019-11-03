import yaml
from pddl_helper import * 

class EDMMWriter:

	def __init__(self, initial_file, types, filename):
		self.initial_file = initial_file
		self.types = types
		self.filename = filename
		self.data = None

	def write_to_file(self):
		with open(self.filename, 'w+') as outfile:
			yaml.dump(self.data, outfile, default_flow_style=False)

	def generate_keyword_list(self,content):
		local_list = []
		for key, value in content.items():
			local_list.append(key)
			local_list.extend(self.generate_keyword_list(value))
		return local_list

	def generate_edmm(self, topology):
		initial_content = yaml.safe_load(open(str(self.initial_file), "r"))
		keywords = list(initial_content["components"].keys())
		for component in initial_content["components"]:
			keywords.append(initial_content["components"][component]["type"])
		keywords += list(self.types.keys())

		# dict which contains pddl compliant keywords as keys and actually
		# used keywords in edmm as values
		keyword_converter = dict()
		for keyword in keywords:
			keyword_converter[to_pddl_compliant_name(keyword)] = keyword

		components = dict()
		for component in topology.components:
			components[keyword_converter[component.u_name]] = dict(
				type = keyword_converter[component.component_type.u_name])

		for connection in topology.connections:
			if not "relations" in components[connection[0].u_name]:
				components[keyword_converter[connection[0].u_name]]["relations"] = [keyword_converter[connection[1].u_name]]
			else:
				components[keyword_converter[connection[0].u_name]]["relations"].append(keyword_converter[connection[1].u_name])


		self.data = initial_content
		initial_content["components"] = components

		# creates dict which compares initial names with actual used names
		self.write_to_file()
