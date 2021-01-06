from subprocess import call

def run_test_cases(code, test_case):
    '''
    1. Create the javascript code for the test cases
    2. Concatenate the javascript code with a js script
    3. Use subprocess to call node process on the concatenated JavaScript code
    4. Node process return results
    5. Return results of test cases for the code
    '''
    # https://codesandbox.io/s/demo-running-user-javascript-code-on-server-securely-and-async-hsz4q
    # call(["node", "path_to_script.js"])

    call(["node", "student/node/runTestcases.js", code])
    pass

run_test_cases('la', 'la')