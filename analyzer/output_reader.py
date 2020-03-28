from parslet import Parslet
import uuid

class Output_Reader:

	def __init__(self):
		self.parslets = []
		self.report = None

	# calls the specified function for the parslet
	def parse_parslet(self, parslet):
		if(len(parslet.snippets_to_parse) == 0): return

		for snippet in parslet.snippets_to_parse:
			parslet.function_to_call(snippet)

	# this function finds the parslet snippets in the output string of the planner
	# in which we are interested in
	# each parslet has a string which describes the start of a parslet
	# and the end of a parslet. The string is a prefix of the specific line
	def parse_output(self, output):
		for line in output.splitlines():
			for parslet in self.parslets:
				# only look at parslets which already contain partial snippets
				if parslet.partial_snippet:
					# parslet does not have a stopping condition 
					# -> finish after first line
					if not parslet.last_line_prefix:
						parslet.save_snippet()
					else:
						parslet.append_to_snippet(line + "\n")

						# does the current line satisfy the stopping condition?
						if line.startswith(parslet.last_line_prefix):
							parslet.save_snippet()
				else:
					if line.startswith(parslet.prefix):
						parslet.append_to_snippet(line + "\n")

		for parslet in self.parslets:
			self.parse_parslet(parslet)

		return self.report