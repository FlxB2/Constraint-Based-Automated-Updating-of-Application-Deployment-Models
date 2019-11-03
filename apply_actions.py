from topology import Topology 
from topology import Component
from marvin_actions_reader import read_marvin_actions
from sas_actions_reader import read_sas_actions
from action import Action
import copy

def change_version(topology, types, args):
	change_type(topology, types, args)
	return topology

def change_type(topology, types, args):
	component_name = args[0]
	version_new = args[1]
	component_to_change = None
	initial_component = None
	new_component_type = types[version_new]

	for component in topology.components:
		if component.u_name == component_name:
			component_to_change = component

	initial_component = component_to_change
	component_to_change.component_type = new_component_type

	topology.change_component(initial_component, component_to_change)

	return topology

def connect_nodes(topology, types, args):
	node0 = args[0]
	node1 = args[2]
	comp0 = None
	comp1 = None

	for component in topology.components:
		if component.u_name == node0:
			comp0 = component
		elif component.u_name == node1:
			comp1 = component

	topology.add_connection((comp0, comp1))
	return topology

def disconnect_nodes(topology, types, args):
	node0 = args[0]
	node1 = args[1]

	changed = False

	tmp_connections = topology.connections

	for connection in tmp_connections:
		comp0, comp1 = connection
		if node0 == comp0.u_name and node1==comp1.u_name:
			topology.remove_connection((connection))
			changed = True
			break

	if not changed:
		print("could not find connection " + str(args))

	return topology

def add_node(topology, types, args):
	component_name = args[0]
	version = args[1]
	component_version = None
	changed = False

	for component_type in types:
		print(types[version].u_name + " " + version)
		if types[version].u_name == version:
			component_version = types[version]
			changed = True
			break

	if not changed:
		print("version " + version + " for add node " + component_name + " not found")
		return topology

	topology.add_component(Component(component_name, component_version))
	return topology

def remove_node(topology, types, args):
	component_name = args[0]
	version = args[1]
	changed = False 
	tmp_list = topology.components
	for component in topology.components:
		if component.u_name == component_name:
			tmp_list.remove(component)
			changed = True

	if not changed:
		print("component could not be removed because it is not present " + component_name)

	topology.components = tmp_list
	return topology

def apply_actions(content, topology, types, planner_name):
	if planner_name == "marvin":
		actions = read_marvin_actions(content)
	elif planner_name == "fast_downward":
		actions = read_sas_actions(content)
	else:
		print("EROR: planner " + planner_name + " is not implemented")
		return None
	# create a list of topologies after every step
	# for better visualization
	changed_topologies = []
	applied_actions = []
	changed_topologies.append(topology)
	for action in actions:
		tmp_topology = copy.deepcopy(topology)
		#print("------------------STEP------------------")
		for applied_action in applied_actions:
			tmp_topology = apply_action(applied_action, tmp_topology, types)
		tmp_topology = apply_action(action, tmp_topology, types)
		applied_actions.append(action)
		changed_topologies.append(tmp_topology)

	return changed_topologies

# map action to function
action_to_function = {
	"change_type" : change_version,
	"change_type_by_ancestor" : change_type,
	"connect_components" : connect_nodes,
	"disconnect_components" : disconnect_nodes,
	"add_component" : add_node,
	"remove_component" : remove_node
}

def apply_action(action, topology, types):
	topology = action_to_function[action.name](topology,types, action.args)
	#print(str(topology))
	return topology