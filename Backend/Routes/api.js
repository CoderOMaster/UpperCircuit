const express = require("express");
const router = express.Router();
const Id = require("../models/idProof");
const mongoose = require("mongoose");
const multer = require("multer");
var bodyParser = require("body-parser");
const path = require("path");
const app = express();

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use("/uploads", express.static(path.join(__dirname, "uploads")));

main().catch((err) => console.log(err));
async function main() {
  await mongoose.connect("mongodb://127.0.0.1:27017/messdatabase");
}

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "uploads");
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  },
});

const upload = multer({ storage: storage });

router.post("/upload-photo", upload.array("files", 2), (req, res) => {
  if (!req.files || req.files.length !== 2) {
    return res.send({ error: "Please upload exactly two photos" });
  }

  let p = "localhost:3000/uploads/";
  let file1 = req.files[0];
  let file2 = req.files[1];

  let data = {
    image1: p + file1.filename,
    image2: p + file2.filename,
  };
  const rec = new Id(data);
  rec.save().then(() => {
    console.log("Record Saved");
    res.send({ response: "Record Saved" });
  });
});

module.exports = router;
