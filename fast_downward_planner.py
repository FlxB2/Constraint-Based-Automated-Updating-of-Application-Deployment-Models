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
