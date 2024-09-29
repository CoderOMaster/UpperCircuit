//pic uploading uding multer
const mongoose = require("mongoose");
const express = require('express')
const app = express()
const port = 3000
const path = require('path')

var cors = require('cors')


app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})


app.use(cors({origin: '*'}))

const Id = require('./Routes/api');
app.use('/id',Id);



