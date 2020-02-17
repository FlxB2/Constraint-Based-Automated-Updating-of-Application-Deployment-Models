class Output_Reader:

	parslets = {}
	report = None

	def init(self, output):
		pass 

	# calls the specified function for the parslet
	def parse_parslet(self, parslet):
		parslet.function_to_call(parslet.string_to_parse)

	# this function finds the parslet snippets in the output string of the planner
	# in which we are interested in
	# each parslet has a string which describes the start of a parslet
	# and the end of a parslet. The string is a prefix of the specific line
	def parse_output(self, output):
		self.init(output)

		self.parslets_dict = {parslet.starts_with:parslet for parslet in self.parslets}

		list_open_parslets = []
		list_complete_parslets = []
		for line in output.splitlines():
			for prefix in self.parslets_dict.keys():
				if line.startswith(prefix):
					list_open_parslets.append(self.parslets_dict[prefix])

			for open_parslet in list_open_parslets:
				if line.startswith(open_parslet.ends_with):
					list_open_parslets.remove(open_parslet)
					list_complete_parslets.append(open_parslet)
				open_parslet.string_to_parse += line + "\n"

		for parslet in list_complete_parslets:
			self.parse_parslet(parslet)

		return self.report

# parslets describe the part of the output we are interested in and the correct function
# to parse this part of the planner output
class Parslet:

	starts_with = None
	ends_with = None
	function_to_call = None
	string_to_parse = ""

	def __init__(self, function_to_call, starts_with, ends_with=None):
		self.starts_with = starts_with
		# if no end is given, only one line will be considered
		if ends_with:
			self.ends_with = ends_with
		else:
			self.ends_with = starts_with
		self.function_to_call = function_to_call