'use strict';

var helloworld = require("./helloworld/server");

helloworld.app.listen(8080, function () {
    console.log('Example app listening on port 8080!');
});
