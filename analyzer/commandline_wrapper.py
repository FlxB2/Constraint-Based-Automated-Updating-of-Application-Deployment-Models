import fileinput
import re
from output_reader import Output_Reader
from fast_downward_output_reader import Fast_Downward_Output_Reader
from jasper_output_reader import Jasper_Output_Reader

def parse_planner_output(output):
	# split outputs by delimiter e.g. <<<<FD>>>> or <<<<JASPER>>>>
	fd_output_list = []
	jasper_output_list = []
	current_output = None
	for line in output.splitlines():
		if line.startswith("<<<<FD>>>>"):
			current_output = "FD"
			fd_output_list.append("")
		elif line.startswith("<<<<JASPER>>>>"):
			current_output = "JASPER"
			jasper_output_list.append("")

		if current_output == "FD":
				fd_output_list[len(fd_output_list)-1] += line + "\n"
		elif current_output == "JASPER":
				jasper_output_list[len(jasper_output_list)-1] += line + "\n"

	print("number fd outputs: " + str(len(fd_output_list)))
	print("number jasper outputs: " + str(len(jasper_output_list)))

	reader = Fast_Downward_Output_Reader()
	for output in fd_output_list:
		report = reader.parse_output(output)
		print(report)

	reader = Jasper_Output_Reader()
	for output in jasper_output_list:
		report = reader.parse_output(output)
		print(report)

content = ""
for line in fileinput.input():
	content += line

parse_planner_output(content)