var year = "2017";
var year_dict = [
  { year: 2017, fileName: "/bubble_users_2017.csv" },
  { year: 2018, fileName: "/bubble_users_2018.csv" },
  { year: 2019, fileName: "/bubble_users_2019.csv" }
];
// set the dimensions and margins of the graph
var margin = { top: 10, right: 0, bottom: 30, left: 50 },
  width = 1100;
height = 500 - margin.top - margin.bottom;
var svg = null;
function myFunction() {
  console.log("check data");
  year = document.getElementById("yearSelect").value;
  //document.getElementById("demo").innerHTML = year;
  load_data();
}
load_data();

function init() {
  var node = document.querySelector("#my_dataviz");
  while (node.hasChildNodes()) {
    node.removeChild(node.lastChild);
  }
  // append the svg object to the body of the page
  svg = d3
    .select("#my_dataviz")
    .append("svg")
    .attr("width", width)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
}
//Read the data
function load_data() {
  init();
  var index = year_dict.findIndex(function(e) {
    return e.year === +year;
  });

  var selectedYear = year_dict[index];
  d3.csv(selectedYear.fileName, function(data) {
    console.log(data);

    // Add X axis
    var x = d3
      .scaleLinear()
      .domain([0, 800000])
      .range([0, width]);
    svg
      .append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    //Add label to X axis
    svg
      .append("text")
      .attr("class", "x label")
      .attr("text-anchor", "end")
      .attr("x", width / 2 + 330)
      .attr("y", height + 30)
      .text("Number of Tweets >>");

    // Add Y axis
    var y = d3
      .scaleLinear()
      .domain([0, 500000])
      .range([height, 0]);
    svg.append("g").call(d3.axisLeft(y));

    // Add label for Y axis
    svg
      .append("text")
      .attr("class", "y label")
      .attr("text-anchor", "end")
      .attr("y", 6)
      .attr("dy", ".75em")
      .attr("transform", "rotate(-90)")
      .text("Number of Followers >>");

    // Add a scale for bubble size
    var z = d3
      .scaleLinear()
      .domain([50, 2400])
      .range([4, 40]);

    // Add a scale for bubble color
    var myColor = d3
      .scaleOrdinal()
      .domain(["Asia", "Europe", "Americas", "Africa", "Oceania"])
      .range(d3.schemeSet2);

    // -1- Create a tooltip div that is hidden by default:
    var tooltip = d3
      .select("#my_dataviz")
      .append("div")
      .style("opacity", 0)
      .attr("class", "tooltip")
      .style("background-color", "#A0BED6")
      .style("border-radius", "5px")
      .style("padding", "10px")
      .style("color", "black");

    // -2- Create 3 functions to show / update (when mouse move but stay on same circle) / hide the tooltip
    var showTooltip = function(d) {
      tooltip
        .style("opacity", 1)
        .html(
          "Name: " +
            d.name +
            "<br>" +
            "# Tweets about #MeToo:" +
            d.tweet_count +
            "<br>" +
            "Location:" +
            d.location
        )
        .style("position", "absolute")
        .style("left", d3.mouse(this)[0] + 30 + "px")
        .style("top", d3.mouse(this)[1] + 30 + "px");
    };
    var moveTooltip = function(d) {
      tooltip
        .style("left", d3.mouse(this)[0] + 30 + "px")
        .style("top", d3.mouse(this)[1] + 30 + "px");
    };
    var hideTooltip = function(d) {
      tooltip
        .transition()
        .delay(1000)
        .duration(2000)
        .style("opacity", 0);
    };

    // Add dots
    svg
      .append("g")
      .selectAll("dot")
      .data(data)
      .enter()
      .append("circle")

      .attr("class", "bubbles")
      .attr("cx", function(d) {
        return x(d.total_number_of_tweets);
      })
      .attr("cy", function(d) {
        return y(d.followers_count);
      })
      .attr("r", function(d) {
        return z(d.tweet_count);
      })
      .style("fill", "#640064")
      // -3- Trigger the functions
      .on("mouseover", showTooltip)
      .on("mousemove", moveTooltip)
      .on("mouseleave", hideTooltip);
  });
}
