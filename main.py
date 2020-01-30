from edmm_reader import EDMM_Reader
from topology import Topology
from pddl_generator import Generator
from apply_actions import apply_actions
from pddl_helper import to_pddl_compliant_name
# from graph_widget import GraphWidget
from planner import Planner
from marvin_planner import Marvin
from fast_downward_planner import FastDownward
from edmm_writer import EDMMWriter
import sys
import os
import configparser
from pathlib import Path

# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *

# def gui(changed_topologies):
#     app = QApplication(sys.argv)
#     app.aboutToQuit.connect(app.deleteLater)
#     app.setStyle(QStyleFactory.create("gtk"))
#     screen = GraphWidget(changed_topologies) 
#     screen.show()   
#     sys.exit(app.exec_())

def main():
	config = configparser.ConfigParser()
	config.read('config.ini')
	print("start")
	reader = EDMM_Reader()
	topology, resolved_types = reader.read_edmm(Path(config["FILES"]["input_path"]))

	domain_name = config["DEFAULT"]["domain_name"]
	problem_name = config["DEFAULT"]["problem_name"]

	gen = Generator(domain_name, problem_name)
	goal_state_src = str(Path(config["FILES"]["goal_state"]))
	problem_str = gen.generate_problem(topology, resolved_types, goal_state_src)

	print(problem_str)
	pddl_problem_src = str(Path("pddl/running_example.pddl").resolve())

	# write pddl file
	# with open(str(Path(config["FILES"]["output_pddl_path"])), 'w+') as file:
	# 	file.write(problem_str)

	pddl_domain_src = str(Path(config["PDDL"]["domain_path"]).resolve())

	planner_name = config["DEFAULT"]["planner"]

	if planner_name == "marvin":
		planner = Marvin(pddl_domain_src, pddl_problem_src)
	elif planner_name == "fast_downward":
		planner = FastDownward(pddl_domain_src, pddl_problem_src)
	else:
		print("ERROR planner " + planner_name + " not implemented")
		print("aborting")
		return

	print(planner_name + " OUTPUT \n")
	result = planner.run()
	print(result)

	fixed_resolved_types = {}
	#change resolved types keys to pddl compliant names
	for component_type in resolved_types:
		fixed_resolved_types[to_pddl_compliant_name(component_type)] = resolved_types[component_type]
		fixed_resolved_types[to_pddl_compliant_name(component_type)].u_name = to_pddl_compliant_name(component_type)

	# contains the topology after every applied step
	# last one is the updated topology
	# changed_topologies = apply_actions(result, topology, fixed_resolved_types, planner_name)
	
	# initial_deployment_model_path = str(Path(config["FILES"]["input_path"]))
	# edmm_output_path = str(Path(config["FILES"]["output_path"]))
	# writer = EDMMWriter(initial_deployment_model_path, resolved_types,edmm_output_path)

	# gui(changed_topologies)

if __name__ == "__main__":
	main()