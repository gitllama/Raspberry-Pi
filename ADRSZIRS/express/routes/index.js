var express = require('express');
var exec = require('child_process').exec;
var fs = require('fs');
var yaml = require('js-yaml');

var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  // var data = JSON.parse(fs.readFileSync('./public/remote_layout.json', 'utf8'));
  var data = yaml.load(fs.readFileSync('./public/remote_layout.yml', 'utf8'));
  res.render('index', { 
    title: 'Smart Remote',
    remote_layout : data
  });
});

router.post('/command', function(req, res) {

  var op = (req.query.op).replace(/[+]/g, ' ');
  var cmd = `./public/rust/i2c -c ./public/remote_config.yml ${op}`;
  // var cmd = `python3 ./scripts/send.py ${op}`

  exec(cmd, function(err,stdout,stderr){
    if(err != null){
      res.json({
        result: 'err',
        stdout : stderr
      });
      return;
    }
    res.json({
      result : 'sucess',
      stdout : stdout
    });
  });

});


module.exports = router;
