from planner import Planner
from subprocess import Popen, PIPE
import configparser
from pathlib import Path

class Marvin(Planner):

	def run(self):
		config = configparser.ConfigParser()
		config.read('config.ini')

		path = str(Path(config["EXEC"]["marvin_exec"]).resolve())
		print(Path(config["EXEC"]["marvin_exec"]))

		process = Popen([path, "-b", self.domain_file, self.problem_file], stdout=PIPE)
		(output, err) = process.communicate()
		exit_code = process.wait()
		return output.decode('utf-8') + "\n\n"
