const ivm = require("isolated-vm");

// const code = process.argv[2];
// const testcases = JSON.parse(process.argv[3]);

/*
const code = `
function func() {
	console.log('fuck');
}
`

const testcases = [
  {
      "input": -30,
      "output": -22
  },
  {
      "input": -10,
      "output": 14
  },
  {
      "input": 0,
      "output": 23
  }
];

async function checkResult() {
  // 1. Create the environment
  const isolate = new ivm.Isolate();
  const context = await isolate.createContext();

  // 1. Creates the environment
  try {
    const script = await isolate.compileScript(code);
    await script.run(context);
  } catch (e) {
    console.log(e);
    return;
  }

  // console.log('ba');
  // console.log('bla');
  // console.log(script);

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
    console.log(results);
  } catch (e) {
    console.log(e);
  }
}

checkResult();
*/

const code = "function func() {\n\tconsole.log('fuck');\n\t\n}"
console.log(code.slice(1, -1));
console.log(code.slice(0, -2))
// console.log('fuck');

$(document).ready(function() {
  state = false;
  id = "editable";
  md = "Outside the editor I am **HTML**.   \nAnd inside the editor you see me in **markdown**.   \nMake some edits and again click the button to see the changes as HTML. Wow!";
  var simplemde = new SimpleMDE({
    element: $("textarea#" + id)[0],
    initialValue: md,
  });
  html = simplemde.options.previewRender(md);
  $('#html_container').wrapInner(html);

  $("button").click(function() {
    if (state) {
      $("div#editor_container").css('display', 'none');
      // Show markdown rendered by CodeMirror
      $('#html_container').wrapInner(simplemde.options.previewRender(simplemde.value()));
    } else {
      // Show editor
      $("div#editor_container").css('display', 'inline');
      // Do a refresh to show the editor value
      simplemde.codemirror.refresh();
      $('#html_container').empty();
    };
    state = !state;
  });
});


(function() {
  var state = false;
  var id = "editable";
  var md = "Outside the editor I am **HTML**.   \nAnd inside the editor you see me in **markdown**.   \nMake some edits and again click the button to see the changes as HTML. Wow!";
  var simplemde = new SimpleMDE({
    element: document.getElementById(id),
    initialValue: md
  });
  var html = simplemde.options.previewRender(md);
  document.getElementById('html_container').innerHTML = html;

  document.getElementById('button').onclick = function() {
    if (state) {
      document.getElementById('editor_container').style.display = 'none';
      document.getElementById('html_container').innerHTML = simplemde.options.previewRender(simplemde.value());
    } else {
      document.getElementById('editor_container').style.display = 'inline';
      simplemde.codemirror.refresh();
      document.getElementById('html_container').empty();
    }
    state = !state;
  }
})();