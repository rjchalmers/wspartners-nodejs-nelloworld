'use strict';

var supertest = require('supertest');
var mocha = require('mocha');
var helloworld = require('../helloworld/server');

var app = helloworld.app;

describe('GET /', function() {
    it('responds with status 200', function(done) {
        supertest(app)
        .get("/")
        .expect(200)
        .end(done);
    });
});
