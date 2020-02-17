from output_reader import Output_Reader
from output_reader import Parslet
from report import Report

class Fast_Downward_Output_Reader(Output_Reader):

	planner_name = "fast_downward"

	def init(self, output):
		self.report = Report("test", self.planner_name)

	def parse_plan(plan_string):
		pass
		

	def parse_whole_result(result_string):
		pass

	def parse_arguments(argument_string):
		pass


	parslets = [Parslet(parse_plan, "Solution found!", "Plan cost:"), 
				Parslet(parse_whole_result, "Search time:", "Solution found."),
				Parslet(parse_arguments, "INFO     search command line string:")]
	parslets_dict = {}