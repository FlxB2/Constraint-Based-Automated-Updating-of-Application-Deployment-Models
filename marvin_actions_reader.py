import re 
from action import Action

def read_action_output(output):
	actions = []
	reached_actions = False
	for line in output.split("\n"):
		# ignore empty lines
		if line.strip():
			# find beginning of action output
			if line.startswith(";;;;"):
				reached_actions = True
			# ignore comments
			if reached_actions and not line.startswith(";"):
				line = line.lstrip('0123456789:( ')
				line = re.sub(r'\)\s*\[[0-9]+\]$', '', line)
				name, args = read_action(line)
				#print(name + " " + args)
				if name is not None and args is not None:
					actions.append(Action(name, args))
	return actions

def read_action(line):
	# actions are represented in a dictionary
	# action type as the key
	# the value is a list containg the arguments
	action = {}

	tokens = line.split()
	print(tokens)
	args = tokens[1:]
	name = tokens[0]
	if len(args) == 0:
		print("ERROR reading action " + name + " no arguments provided")
	return name, args

def read_marvin_actions(src):
	return read_action_output(src)