const ivm = require("isolated-vm");

const code = process.argv[2]
              .slice(1, -1)
              .replace(/\\n/g, '\n')
              .replace(/\\t/g, '\t');
const testcases = JSON.parse(process.argv[3]);

async function checkResult() {
  // 1. Create the environment
  const isolate = new ivm.Isolate();
  const context = await isolate.createContext();

  // 1. Creates the environment
  try {
    const script = await isolate.compileScript(code);
    await script.run(context);
  } catch (e) {
    console.log('Error');
    return;
  }

  try {
    const fnRef = await context.global.get('func');
    const results = [];
    for (let i = 0; i < testcases.length; i++) {
      const { input, output } = testcases[i];
      const userOutput = await fnRef.apply(undefined, [input]);
      const result = {
        isMatch: JSON.stringify(userOutput) === JSON.stringify(output),
        userOutput: userOutput
      }
      results.push(result);
    }
    console.log(JSON.stringify(results));
  } catch (e) {
    console.log('Error');
  }
}

checkResult();