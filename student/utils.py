import json
from subprocess import PIPE, run

'''
UTILITIES FOR RUNNING USER CODE
'''
def run_testcases(code, testcases):
    '''
    Return results of testcases
    Example output: [
        {'isMatch': false, 'userOutput': 0},
        {'isMatch': false, 'userOutput': 0},
        {'isMatch': false, 'userOutput': 0}
    ]
    '''
    command = ["node", "student/node/runTestcases.js", code, testcases]
    output = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    try:
        return json.loads(output.stdout)
    except:
        return {'Error': True}


def is_testcases_pass(results):
    if results == {'Error': True}:
        return False
    else:
        for result in results:
            if not result['isMatch']:
                return False
    return True


