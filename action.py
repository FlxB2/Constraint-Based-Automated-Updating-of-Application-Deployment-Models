class Action:
	def __init__(self, name, args):
		self.name = name
		self.args = args

	def __str__(self):
		return "ACTION " + self.name + " - args - " + str(self.args) 