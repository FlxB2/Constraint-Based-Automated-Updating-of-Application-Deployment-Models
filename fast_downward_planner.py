from planner import Planner
from subprocess import Popen, PIPE
import configparser
from pathlib import Path

class FastDownward(Planner):

	def run(self):
		config = configparser.ConfigParser()
		config.read('config.ini')

		path = str(Path(config["EXEC"]["fast_downward_exec"]).resolve())
		print(Path(config["EXEC"]["fast_downward_exec"]))

		planner_options = config["EXEC"]["fast_downward_options"]

		if planner_options == "fFyY":
			process = Popen(["python3", path, self.domain_file, self.problem_file,
				'--evaluator', "hff=ff()", '--evaluator', "hcea=cea()",
				'--search', "lazy_greedy([hff, hcea], preferred=[hff, hcea])"])
		elif planner_options == "fF":
			process = Popen(["python3", path, self.domain_file, self.problem_file,
				'--evaluator', "hff=ff()",
				'--search', "lazy_greedy([hff], preferred=[hff])"])
		elif planner_options == "yY":
			process = Popen(["python3", path, self.domain_file, self.problem_file,
				'--evaluator', "hcea=cea()",
				'--search', "lazy_greedy([hcea], preferred=[hcea])"])
		elif planner_options == "landmark-cut":
			process = Popen(["python3", path, self.domain_file, self.problem_file, '--search', "astar(lmcut())"])
		elif planner_options == "iPDB":
			process = Popen(["python3", path, self.domain_file, self.problem_file, '--search', "astar(ipdb())"])
		else:
			process = Popen(["python3", path, self.domain_file, self.problem_file, '--search', "astar(blind())"])

		print(str(process))
		(output, err) = process.communicate()
		exit_code = process.wait()

		# pick plan
		# for now - just pick the first plan
		# future work: pick plan with heuristics
		if Path("sas_plan").exists():
			plan_path = Path("sas_plan")
		else:
			plan_path = Path("sas_plan.1")
		content = ""

		with open(str(plan_path), 'r') as content_file:
			content = content_file.read()

		return content
