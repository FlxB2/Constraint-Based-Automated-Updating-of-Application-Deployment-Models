from action import Action 

def read_action(line):
	# actions are represented in a dictionary
	# action type as the key
	# the value is a list containg the arguments
	action = {}

	tokens = line.split()
	args = tokens[1:]
	name = tokens[0]
	if len(args) == 0:
		print("ERROR reading action " + name + " no arguments provided")
	return name, args


def read_line(line):
	# remove leading and trailing whitespace / tabs
	line.lstrip()
	line.rstrip()

	if(line[0] == ';') or len(line.strip()) == 0:
		# can be used later to read cost
		return (None, None)
	elif(line[0] == '('):
		# removes leading ( and trailing ) \n
		print(line[1:-2])
		return read_action(line[1:-1])
	else:
		return (None, None)

def read_sas_actions(content):
	actions = []
	print(content)
	for line in content.splitlines():
		name, args = read_line(line)
		if name is not None and args is not None:
			actions.append(Action(name, args))
	return actions