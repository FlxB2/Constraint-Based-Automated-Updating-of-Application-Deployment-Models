import fileinput
from output_reader import Output_Reader
from fast_downward_output_reader import Fast_Downward_Output_Reader

content = ""
for line in fileinput.input():
	content += line

# start utility
reader = Fast_Downward_Output_Reader()
report = reader.parse_output(content)

print(str(report))