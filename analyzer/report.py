class Plan:

	def __init__(self, name, execution_time, number_steps, steps):
		self.name = name
		# time in seconds!
		self.execution_time = execution_time
		self.number_steps = number_steps
		self.steps = steps

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
		execution_times = {plan.execution_time:plan for plan in self.plans}
		result_key = execution_times.keys().sort()[n]
		return execution_times[result_key]

	# calculates for n=1 plan with fewest steps
	# for n = len(self.plans) plan with the most steps
	# for n = 2 the plant with 2nd fewest steps etc
	def nth_plan_by_steps(self, n):
		# array starts with zero
		n = n-1
		execution_times = {plan.number_steps:plan for plan in self.plans}
		result_key = execution_times.keys().sort()[n]
		return execution_times[result_key]

	def add_line(self, line):
		return line + "\n"

	def add_indented_line(self, line):
		return "\t" + line + "\n"

	def __str__(self):
		rep = ""
		if self.name: rep += self.add_line("REPORT " + self.name)
		if self.planner_name: rep += self.add_line("using planner: " + self.planner_name)
		if self.planner_arguments: rep += self.add_line("parameters: " + self.parameters)
		if self.solution_found: rep += self.add_line("solution found")
		if self.execution_time: rep += self.add_line("whole execution time: " + self.execution_time)

		# prints fastest and slowest plan
		if len(self.plans) > 0:
			rep += self.add_line("FASTEST PLAN:")
			rep += self.add_indented_line(str(self.nth_plan_by_exec_time(1)))
		elif len(self.plans) > 1:
			rep += self.add_line("SLOWEST PLAN:")
			rep += self.add_indented_line(str(self.nth_plan_by_exec_time(len(self.plans))))

		# prints plans with most and fewest steps
		if len(self.plans) > 0:
			rep += self.add_line("FEWEST STEPS PLAN:")
			rep += self.add_indented_line(str(self.nth_plan_by_steps(1)))
		elif len(self.plans) > 1:
			rep += self.add_line("MOST STEPS PLAN:")
			rep += self.add_indented_line(str(self.nth_plan_by_steps(len(self.plans))))

		return rep




