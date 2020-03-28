class Plan:

	def __init__(self, execution_time, number_steps, 
				actions, cost="", name="", arguments=""):
		self.name = name
		# time in seconds!
		self.execution_time = execution_time
		self.number_steps = number_steps
		self.cost = cost
		self.actions = actions
		self.arguments = arguments

	def __str__(self):
		res =  ("PLAN " + self.name + "\n"
			+ "exec time " + str(self.execution_time) + "s\n"
			+ "number steps " + str(self.number_steps) + "\n")

		if self.arguments != "":
			res += "arguments " + self.arguments + "\n"

		for action in self.actions.splitlines():
			res += "\t" + action + "\n"
		return res

class Report:

	def __init__(self, name, planner_name):
		self.name = name
		self.planner_name = planner_name

		self.planner_arguments = None
		self.solution_found = False
		self.execution_time = None

		self.plans = []

	# calculates for n=1 fastest plan
	# for n = len(self.plans) the slowest plan
	# for n = 2 the 2nd fastest plan etc
	def nth_plan_by_exec_time(self, n):
		# array starts with zero
		n = n-1
		if n >= len(self.plans)-1: n = len(self.plans)-1
		execution_times = {plan.execution_time:plan for plan in self.plans}
		result_key = sorted([float(k) for k in execution_times])[n]
		return execution_times[str(result_key)]

	# calculates for n=1 plan with fewest steps
	# for n = len(self.plans) plan with the most steps
	# for n = 2 the plant with 2nd fewest steps etc
	def nth_plan_by_steps(self, n):
		# array starts with zero
		n = n-1
		if n >= len(self.plans)-1: n = len(self.plans)-1
		execution_times = {plan.number_steps:plan for plan in self.plans}
		result_key = sorted([int(k) for k in execution_times])[n]
		return execution_times[str(result_key)]

	def add_line(self, line):
		return line + "\n"

	def add_indented_line(self, line):
		return "\t" + self.add_line(line)

	def __str__(self):
		rep = "REPORT \n"
		if self.name: rep += self.add_line("name: " + self.name)
		if self.planner_name: rep += self.add_line("using planner: " + self.planner_name)
		if self.planner_arguments: rep += self.add_line("parameters: " + self.planner_arguments)
		if self.solution_found: rep += self.add_line("solution found")
		if self.execution_time: rep += self.add_line("whole execution time: " + self.execution_time +"s")

		# prints fastest and slowest plan
		if len(self.plans) > 0:
			rep += self.add_line("FASTEST PLAN TO CALCULATE:")
			plan = str(self.nth_plan_by_exec_time(1))
			for line in plan.splitlines():
				rep += self.add_indented_line(line)
		elif len(self.plans) > 1:
			rep += self.add_line("SLOWEST PLAN:")
			plan = str(self.nth_plan_by_exec_time(1))
			for line in plan.splitlines():
				rep += self.add_indented_line(line)

		# prints plans with most and fewest steps
		if len(self.plans) > 0:
			rep += self.add_line("FEWEST STEPS PLAN:")
			plan = str(self.nth_plan_by_steps(1))
			for line in plan.splitlines():
				rep += self.add_indented_line(line)
		elif len(self.plans) > 1:
			rep += self.add_line("MOST STEPS PLAN:")
			plan = str(self.nth_plan_by_steps(1))
			for line in plan.splitlines():
				rep += self.add_indented_line(line)

		return rep




