from output_reader import Output_Reader
from parslet import Parslet
from report import Report
from report import Plan
import re

class Jasper_Output_Reader(Output_Reader):

	planner_name = "jasper"

	def __init__(self):
		self.report = Report("jasper", self.planner_name)
		self.parslets = [Parslet(self.parse_plan, "Starting search:", "Starting search:"),
		Parslet(self.parse_time, "Search time:")]

	# Example parslet:
	# 	Solution found!
	# 	Actual search time: 4.8324s [t=4.84568s]
	# 	change_type ubuntu1 ubuntu-12xx04 ubuntu-18xx04 (1)
	# 	...
	# 	change_type java-runtime0 java_runtime-6 java_runtime-8 (1)
	# 	Plan length: 5 step(s).
	# 	Plan cost: 5
	def parse_plan(self, args):
		if(not "plan_id" in args): return

		self.solution_found = True
		lines = args.splitlines()
		exec_time = -1
		plan_length = -1
		plan_cost = -1
		plan_start_index = 0
		plan_end_index = 0
		counter = 0
		for line in lines:
			if("Real Total time" in line):
				plan_start_index = counter+1
			elif("Plan length" in line and plan_end_index == 0):
				plan_end_index = counter
				plan_length = re.findall(r'\d', line)[0]
			elif("Plan cost" in line):
				plan_cost = re.findall(r'\d', line)[0]
			elif("Actual search time:" in line):
				exec_time = re.findall(r'\d+\.\d+', line)[0]
			counter+=1				

		actions = "\n".join(lines[plan_start_index:plan_end_index])
		plan = Plan(exec_time, plan_length, plan_cost, actions, str(len(self.report.plans)))
		self.report.plans.append(plan)

	# Example parslet:
	#	Search time: 4.83256s
	def parse_time(self, args):
		search_time = re.search(r'\d+\.\d+', args).group(0)		
		self.report.execution_time = search_time





		
		
