var express = require("express");
var app = express();
var router = express.Router();
var path = __dirname + "/views/";

router.use(function(req, res, next) {
  console.log("/" + req.method);
  next();
});

router.get("/", function(req, res) {
  res.sendFile(path + "index.html");
});

router.get("/word_cloud", function(req, res) {
  res.sendFile(path + "word_cloud.html");
});

// router.get("/contact", function(req, res) {
//   res.sendFile(path + "contact.html");
// });

router.get("/bubble_users_2017.csv", function(req, res) {
  res.sendFile(path + "/csv/bubble_users_2017.csv");
});
router.get("/bubble_users_2018.csv", function(req, res) {
  res.sendFile(path + "/csv/bubble_users_2018.csv");
});
router.get("/bubble_users_2019.csv", function(req, res) {
  res.sendFile(path + "/csv/bubble_users_2019.csv");
});
router.get("/tweet_text.csv", function(req, res) {
  res.sendFile(path + "/csv/tweet_text.csv");
});

app.use("/public", express.static("public"));

app.use("/", router);

app.use("*", function(req, res) {
  res.sendFile(path + "404.html");
});

const PORT = process.env.PORT || 3000;

var server = app.listen(PORT, function() {
  console.log("app running on port.", PORT);
});
