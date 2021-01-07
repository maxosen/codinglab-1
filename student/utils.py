import json
from subprocess import PIPE, run

def run_testcases(code, testcases):
    command = ["node", "student/node/runTestcases.js", code, testcases]
    output = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    try:
        return json.loads(output.stdout)
    except:
        return {'Error': True}
