const mongoose =require('mongoose');
const {Schema} = mongoose;


const idSchema= new Schema({
    image: {type:String, required:true}
})

module.exports=mongoose.model('Id',idSchema);