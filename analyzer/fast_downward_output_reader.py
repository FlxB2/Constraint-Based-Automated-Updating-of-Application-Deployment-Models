from output_reader import Output_Reader
from output_reader import Parslet
from report import Report
from report import Plan
import re

class Fast_Downward_Output_Reader(Output_Reader):

	planner_name = "fast_downward"

	def init(self, output):
		self.report = Report("fast_downward", self.planner_name)
		self.parslets = [Parslet(self.parse_plan, "Solution found!", "Plan cost:"), 
				Parslet(self.parse_time, "Search time:"),
				Parslet(self.parse_arguments, "INFO     search command line string:")]

	# Example parslet:
	# 	Solution found!
	# 	Actual search time: 4.8324s [t=4.84568s]
	# 	change_type ubuntu1 ubuntu-12xx04 ubuntu-18xx04 (1)
	# 	...
	# 	change_type java-runtime0 java_runtime-6 java_runtime-8 (1)
	# 	Plan length: 5 step(s).
	# 	Plan cost: 5
	def parse_plan(self, args):
		self.solution_found = True
		lines = args.splitlines()
		exec_time = re.search(r'\d+\.\d+', lines[1]).group(0)
		plan_length = re.findall(r'\d', lines[-2])[0]
		plan_cost = re.findall(r'\d', lines[-1])[0]
		actions = ""
		for i in range(2,len(lines)-2):
			actions += re.sub(r'\(.*\)', "", lines[i]) + "\n"
		plan = Plan(exec_time, plan_length, plan_cost, actions, str(len(self.report.plans)))
		self.report.plans.append(plan)
		
		
	# Example parslet:
	#	Search time: 4.83256s
	def parse_time(self, args):
		lines = args.splitlines()
		search_time = re.search(r'\d+\.\d+', lines[0]).group(0)		
		self.report.execution_time = search_time

	# Example parslet:
	# INFO     search command line string: /some/path/downward --search 'astar(blind())' 
	def parse_arguments(self, args):
		argument_list = args.split()[6:]
		self.report.planner_arguments = " ".join(argument_list)