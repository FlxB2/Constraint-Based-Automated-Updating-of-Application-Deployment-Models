import uuid

class Output_Reader:

	parslets = {}
	parslets_dict = {}
	report = None

	def init(self, output):
		pass 

	# calls the specified function for the parslet
	def parse_parslet(self, parslet):
		if(len(parslet.snippets_to_parse) == 0): 
			return

		for snippet in parslet.snippets_to_parse:
			parslet.function_to_call(snippet)

	# this function finds the parslet snippets in the output string of the planner
	# in which we are interested in
	# each parslet has a string which describes the start of a parslet
	# and the end of a parslet. The string is a prefix of the specific line
	def parse_output(self, output):
		self.init(output)

		self.parslets_dict = {parslet.prefix:parslet for parslet in self.parslets}

		open_parslets = []
		for line in output.splitlines():
			for open_parslet in open_parslets:
				open_parslet.append_to_snippet(line + "\n")

				if line.startswith(open_parslet.last_line_prefix):
					if(not (open_parslet.prefix == open_parslet.last_line_prefix and 
						len(open_parslet.partial_snippet.splitlines()) == 1)):
						open_parslet.save_snippet()
						open_parslets.remove(open_parslet)

			for prefix in self.parslets_dict.keys():
				if (line.startswith(prefix) and 
					not self.parslets_dict[prefix] in open_parslets):
					self.parslets_dict[prefix].append_to_snippet(line + "\n")
					open_parslets.append(self.parslets_dict[prefix])

		for parslet in self.parslets_dict.values():
			self.parse_parslet(parslet)

		return self.report

# parslets describe the part of the output we are interested in and the correct function
# to parse this part of the planner output
class Parslet:
	prefix = None
	last_line_prefix = None
	function_to_call = None
	snippets_to_parse = []
	partial_snippet = ""

	def __init__(self, function_to_call, prefix, last_line_prefix=None):
		self.prefix = prefix
		# if no end is given, only one line will be considered
		if last_line_prefix:
			self.last_line_prefix = last_line_prefix
		else:
			self.last_line_prefix = prefix
		self.function_to_call = function_to_call

	def append_to_snippet(self, content):
		self.partial_snippet += content

	def save_snippet(self):
		self.snippets_to_parse.append(self.partial_snippet)
		self.partial_snippet = ""
