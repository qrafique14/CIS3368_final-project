// First I made the necessary imports and initializations 
var express = require('express');
// for building the endpoints
var app = express();
// needed for express
const bodyParser  = require('body-parser');
// Rest api libary
const axios = require('axios');
const { response } = require('express');
app.use(bodyParser.urlencoded());
// tells the app the template engine
app.set('views', __dirname + '/views')
app.set('view engine', 'ejs');
const server_ip = '127.0.0.1:5000'
const auth = false
app.get('/', function (req, res) {
    res.render('pages/login', {auth: ''})
})
app.post('/', function(req, res) {
    user = req.body['username']
    passwd = req.body['password']
    console.log(user)
    axios.get(server_ip + '/api/login', {}, { auth: {username: user, password: passwd}})
    .then((response)=>{
        console.log(response.data)
        if (response.status == 200){
                auth = true
                console.log('yess')
                // res.redirect('/trips')
        }
        res.redirect('/trips')
    }).catch(api => api)
})
app.get('/trips', function (req, res) {
    axios.get('http://127.0.0.1:5000/api/trips')
    .then((response)=>{
        let trips = response.data;
        res.render('pages/trips', {
            // renders the page and passes the var of the response
            trips: trips
        });
    })
    
})

app.get('/create', function(req, res) {
    res.render('pages/create')
})

app.post('/edit', function (req, res) {
    id = req.body.id
    trip_name = req.body['name']
    trans = req.body['trans']
    des = req.body['des']
    sd = req.body['sd']
    ed = req.body['ed']
    axios.put('http://127.0.0.1:5000/api/trips', {des,trans,sd,ed,trip_name,id})
    
})

app.listen(8080);
console.log('8080 is the magic port');