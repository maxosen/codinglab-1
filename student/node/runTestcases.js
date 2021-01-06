const ivm = require("isolated-vm")

console.log(process.argv);
// const { usercode } = req.body;
// const { problem } = req.params;

// 1. create the environment
let isolate = new ivm.Isolate();
let context = await isolate.createContext();
try {
  let script = await isolate.compileScript(usercode);
  await script.run(context);
} catch (e) {
  res.json(createErrorJson(e));
  return;
}

// 2. run the code, and await the result
try {
  let fnReference = await context.global.get("problem");
  const results = [];
  for (let i = 0; i < testcases.length; i++) {
    const input = testcases[i][0];
    const output = await fnReference.apply(undefined, input);
    results.push(JSON.stringify(output) === JSON.stringify(testcases[i][1]));
  }
  res.json(`{"result": ${results}}`);
} catch (e) {
  res.json(createErrorJson(e));
  return;
}