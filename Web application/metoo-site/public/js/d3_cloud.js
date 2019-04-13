//Simple animated example of d3-cloud - https://github.com/jasondavies/d3-cloud
//Based on https://github.com/jasondavies/d3-cloud/blob/master/examples/simple.html

// Encapsulate the word cloud functionality
function wordCloud(selector) {
  // var fill = d3.scale.category20();
  var fill = d3.scaleOrdinal(d3.schemeCategory20);

  //Construct the word cloud's SVG element
  var svg = d3
    .select("#word_cloud_graph")
    .append("svg")
    .attr("width", 500)
    .attr("height", 500)
    .append("g")
    .attr("transform", "translate(250,250)");

  //Draw the word cloud
  function draw(words) {
    var cloud = svg.selectAll("g text").data(words, function(d) {
      return d.text;
    });

    //Entering words
    cloud
      .enter()
      .append("text")
      .style("font-family", "Impact")
      .style("fill", function(d, i) {
        return fill(i);
      })
      .attr("text-anchor", "middle")
      .attr("font-size", 15)
      .text(function(d) {
        return d.text;
      });

    //Entering and existing words
    cloud
      .transition()
      .duration(600)
      .style("font-size", function(d) {
        return 15 + d.size + "px";
      })
      .attr("transform", function(d) {
        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
      })
      .style("fill-opacity", 1);

    //Exiting words
    cloud
      .exit()
      .transition()
      .duration(200)
      .style("fill-opacity", 1e-6)
      .attr("font-size", 15)
      .remove();
  }

  //Use the module pattern to encapsulate the visualisation code. We'll
  // expose only the parts that need to be public.
  return {
    //Recompute the word cloud for a new set of words. This method will
    // asycnhronously call draw when the layout has been computed.
    //The outside world will need to call this function, so make it part
    // of the wordCloud return value.
    update: function(words) {
      d3.layout
        .cloud()
        .size([500, 500])
        .words(words)
        .padding(5)
        .rotate(function() {
          return ~~(Math.random() * 2) * 90;
        })
        .font("Impact")
        .fontSize(function(d) {
          return 15 + d.size;
        })
        .on("end", draw)
        .start();
    }
  };
}

//Create a new instance of the word cloud visualisation.
var myWordCloud = wordCloud("body");
var words = [];

// Get the data
d3.csv("/tweet_text.csv", function(error, data) {
  if (error) throw error;
  console.log(data);
  // format the data
  words = data.map(function(d) {
    return d.lemma_filter;
  });
  //Start cycling through the demo data
  showNewWords(myWordCloud);
});

//Prepare one of the sample sentences by removing punctuation,
// creating an array of words and computing a random size attribute.
function getWords(i) {
  return words[i]
    .replace(/[!\.,:;\?]/g, "")
    .split(" ")
    .map(function(d) {
      return { text: d, size: 10 + Math.random() * 60 };
    });
}

//This method tells the word cloud to redraw with a new set of words.
//In reality the new words would probably come from a server request,
// user input or some other source.
function showNewWords(vis, i) {
  i = i || 0;

  vis.update(getWords(i++ % words.length));
  setTimeout(function() {
    showNewWords(vis, i + 1);
  }, 2000);
}
