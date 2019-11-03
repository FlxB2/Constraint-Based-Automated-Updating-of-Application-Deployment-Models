from topology import Topology
from pddl_helper import Problem
from pathlib import Path
import re

class Generator:

	problem = None
	added_parents = []

	def __init__(self, domain_name, problem_name):
		self.problem = Problem(domain_name, problem_name)

	def add_used_component_types(self, topology):
		for component in topology.components:
			version = component.component_type
			self.problem.add_init_predicate("is_used", component.u_name)
			self.problem.add_init_predicate("has_type", component.u_name, version.u_name)
			self.problem.add_object(component.u_name, "component")

	def add_type(self, component_type):
		parent = component_type.parent
		name = component_type.u_name

		if not name in self.added_parents:
			self.problem.add_object(component_type.u_name, "abstract_component_type")
			self.added_parents.append(name)

			if parent is not None:
				self.problem.add_init_predicate("has_parent_type", name, parent.u_name)
				self.add_type(parent)

	def get_versions(self, types):
		result = []
		regex = re.compile(r"-([0-9]+[.-]?)+$")
		for component_type in types:
			if re.search(regex, component_type):
				result.append(types[component_type])
		return result

	def add_types(self, topology, types):
		versions = self.get_versions(types)
		added_reqcaps = []

		for version in versions:
			parent = version.parent

			self.problem.add_object(version.u_name, "component_type")

			for req in version.reqs or []:
				self.problem.add_init_predicate("has_requirement", version.u_name, req)
				if req not in added_reqcaps:
					self.problem.add_object(req , "reqcap")
					added_reqcaps.append(req)

			for cap in version.caps or []:
				self.problem.add_init_predicate("has_capability", version.u_name, cap)
				if cap not in added_reqcaps:
					self.problem.add_object(cap, "reqcap")
					added_reqcaps.append(cap)

			if parent is not None:
				self.problem.add_init_predicate("has_abstract_type", version.u_name, parent.u_name)
				self.add_type(parent)

	def add_connections(self, topology):
		for connection in topology.connections:
			print("CONNECTION " + str(connection))
			self.problem.add_init_predicate("connected_with", connection[0].u_name, connection[1].u_name)


	def generate_goal(self, topology,goal_src):
		for component in topology.components:
			version = component.component_type
			self.problem.add_goal_predicate("is_used", component.u_name)

		self.problem.add_user_goal(goal_src)

	def generate_problem(self, topology, types, goal_src):
		self.add_used_component_types(topology)
		self.add_types(topology, types)
		self.add_connections(topology)
		self.generate_goal(topology,goal_src)

		return self.problem.getString()