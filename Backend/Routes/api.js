const express= require('express');
const router=express.Router();
const Id=require('../models/idProof');
const mongoose=require('mongoose');
const multer  = require('multer')
var bodyParser = require('body-parser')
const path = require('path')
const app = express()

app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())



app.use('/uploads', express.static(path.join(__dirname, 'uploads')))

main().catch((err) => console.log(err));
async function main() {
  await mongoose.connect("mongodb://127.0.0.1:27017/messdatabase");
}

const storage = multer.diskStorage({ 
  destination: function (req, file, cb) {
    cb(null, 'uploads')
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname)
  }
})

const upload = multer({ storage: storage })

router.post('/upload-photo',upload.single('file'),(req,res)=>{
  console.log(req.file);
  let p="localhost:3000/uploads/"
  let data={
    image : p+req.file.filename
  }
  const rec= new Id(data);
  rec.save().then(()=>{console.log('Record Saved'); res.send({response:'Record Saved'})});

})

module.exports=router;