from output_reader import Output_Reader
from report import Report

class Fast_Downward_Output_Reader(Output_Reader):

	planner_name = "fast_downward"

	def parse_output(self, output):
		report = Report("test", self.planner_name)


		return report

