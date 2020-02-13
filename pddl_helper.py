import re

class Problem:

	def __init__(self, domain_name, name):
		self.domain_name = domain_name
		self.name = name
		self.objects = ""
		self.init = ""
		self.goal = ""

	def xstr(self, s):
		return '' if s is None else str(s)

	def insert_line(self, string):
		return to_pddl_compliant_name(string) + "\n"

	def insert_predicate(self, string):
		return self.insert_line("( " + string + " )")

	def add_object(self, name, object_type):
		self.objects += self.insert_line(name + " - " + object_type)

	def add_init_predicate(self, predicate_name, arg0, arg1=None):
		self.init += self.insert_predicate(predicate_name + " " + arg0 + " " + self.xstr(arg1))

	def add_goal_predicate(self, predicate_name, arg0, arg1=None):
		self.goal += '\t' + self.insert_predicate(predicate_name + " " + arg0 + " " + self.xstr(arg1))

	def add_user_goal(self, path):
		content = open(path)
		user_goal = ""
		for line in content:
			user_goal += "\n\t" + to_pddl_compliant_name(line.strip())
		self.goal += user_goal

	def getString(self):
		# pretty print
		init_list = self.init.splitlines(True)
		init_list.sort()
		objects_list = self.objects.splitlines(True)
		objects_list.sort(key=lambda x: (x[::-1], len(x)))
		self.objects='\t\t'.join(objects_list)
		self.init='\t\t'.join(init_list)
		self.goal='\t\t'.join(self.goal.splitlines(True))

		return ("(define (problem " + self.name + ")\n" + 
			"\t(:domain " + self.domain_name + ")\n" +
			"\t(:objects \n\t\t" + self.objects + "\t)\n" + 
			"\t(:init \n\t\t" + self.init + "\t)\n" + 
			"\t(:goal \n\t\t" + "(and (check_all_nodes) \n\t\t"
				 + self.goal +  "\n\t\t)\n\t)\n)")


def to_pddl_compliant_name(name):
	#pddl only supports [a-zA-Z0-9][-_] in names
	name = re.sub(r"[^() \ta-zA-Z0-9-_]+", "XX", name)
	name = name.lower()
	return name