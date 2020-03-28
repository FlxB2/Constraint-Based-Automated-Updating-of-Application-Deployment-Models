# parslets describe the part of the output we are interested in and the correct function
# to parse this part of the planner output
class Parslet:

	def __init__(self, function_to_call, prefix, last_line_prefix=None):
		self.prefix = prefix
		# if no end is given, only one line will be considered
		if last_line_prefix:
			self.last_line_prefix = last_line_prefix
		else:
			self.last_line_prefix = None

		self.function_to_call = function_to_call
		self.snippets_to_parse = []
		self.partial_snippet = None


	def append_to_snippet(self, content):
		if not self.partial_snippet:
			self.partial_snippet = ""
		self.partial_snippet += content

	def save_snippet(self):
		self.snippets_to_parse.append(self.partial_snippet)
		self.partial_snippet = None
