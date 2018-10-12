'use strict';

// http://expressjs.com/en/starter/hello-world.html
var express = require('express');
var app = express();

app.get('/', function (req, res) {
    res.send('Hello world from Node ' + process.version + '!\n');
});

// /status is used by ELB health checkers to assert that the service is running OK
app.get('/status', function (req, res) {
    res.send("OK");
});

// We do the "listen" call in index.js - making this module easier to test

module.exports.app = app;
