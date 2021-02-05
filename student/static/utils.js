function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}

function chunk(ar1, len) {
  var chunks = [],
      i = 0,
      n = ar1.length;
  while (i < n) {
    chunks.push(ar1.slice(i, i += len));
  }
  return chunks;
}

function chunk2(arr, len) {
  var chunks = []
  var numOfGroups = Math.ceil(arr.length / len)
  for (var i = 0; i < arr.length; i++) {
    var chunk = [];
    for (var j = 0; j < numOfGroups; j++) {
      chunk.push(arr[i]);
    }
    chunks += chunk;
  }
  return chunks;
}

function genHtml(names) {
  var html = '';
  for (var i = 0; i < names.length; i++) {
    var newhtml = ''
    newhtml += `<p>Group ${i+1}</p><ul>`;
    for (var j = 0; j < names[i].length; j++) {
      grouphtml = `<li>${names[i][j]}</li>`;
      newhtml += grouphtml;
    }
    newhtml += `</ul>`;
    html += newhtml;
  }
  return html;
}

function genHtml2(names, size) {
  var html = '';
  for (var i = 0; i < names.length; i++) {
    var newhtml = '';
    if (i === 0) {
      newhtml += `<p>Group ${i+1}</p><ul>`;
    } else if ((i+1) % size === 0) {
      newhtml += `</ul><p>Group ${i+1}</p><ul>`;
    }
    newhtml += `<li>${names[i].length}</li>`;
    html += newhtml;
  }
  return html;
}