var Flint = require('node-flint');
var webhook = require('node-flint/webhook');
var express = require('express');
var bodyParser = require('body-parser');

var app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

// flint options
var config = {
  webhookUrl: process.env.SPARK_WEBHOOKURL,
  token: process.env.SPARK_TOKEN,
  port: process.env.SOILSENSOR_PORT || 8080
};

console.log('config: ' + JSON.stringify(config));

//init flint
var flint = new Flint(config);
// Define markdown as default
flint.messageFormat = 'markdown';
flint.start();


// say hello
flint.hears('hello', function(bot, trigger) {
  console.log('print hello');
  bot.say('Hello **'+trigger.personDisplayName+'**! Print **help** if you need some.');
});

flint.hears('help', function(bot, trigger) {
  console.log('print help');
  bot.say('##I\'m SoilSensor, the bot telling you when your plant needs water.\n'+
          'You can ask me the following commands:\n'+
          '- **get all** will tell you whether to put water or not for all your plants\n'+
          '- **get <sensorId>** will tell you whether to put water from a particular sensor measure\n'+
          '- **help** will print this help');
});


// you can adjust the threshold value
var THRESHOLD_VALUE = 800;

function measureToWaterStatusString(measure) {
  if (measure < THRESHOLD_VALUE) {
    return 'Doesn\'t need watering';
  } else {
    return 'Time to water your plant';
  }
}

function getResponseForSensor(id) {
  return 'Sensor #'+id+': **'+devicesLastMeasures[id]+'** -> '+measureToWaterStatusString(devicesLastMeasures[id]);
}

flint.hears('get', function(bot, trigger) {

  var sensorId = trigger.args[1];
  var response = '**Status of your plants:**\n';

  if (sensorId === 'all') {
    for (id in devicesLastMeasures) {
      response += '- '+getResponseForSensor(id) + '\n';
    }
  }
  else if (devicesLastMeasures.hasOwnProperty(sensorId)) {
    response += '- '+getResponseForSensor(sensorId);
  }
  else {
    response = 'Cannot find sensor #'+sensorId;
  }

  console.log('response: '+response);
  bot.say(response);
});

// default message for unrecognized commands
flint.hears(/.*/, function(bot, trigger) {
  bot.say('Could you please rephrase?');
}, 20);


// define express path for incoming webhooks
app.post('/', webhook(flint));

// Last measures stored per deviceID
var devicesLastMeasures = {
  12345: 50,
  67890: 900
 };

// define express path for incoming sensor notifications
app.post('/soilmoisturesensor/:deviceId', function(req, res) {
  var moistureLevel = req.body.moistureLevel || -1;
  console.log('DevideId: '+ req.params.deviceId +' -> Moisture Level: ' + moistureLevel);

  devicesLastMeasures[req.params.deviceId] = moistureLevel;

  if (moistureLevel >= 0) {
    res.send('OK');
  } else {
    res.send('wrong moistureLevel value ' + moistureLevel);
  }
});

// start express server
var server = app.listen(config.port, function() {
  flint.debug('Flint listening on port %s', config.port);
});

server.on('error', onError);
server.on('listening', onListening);

/**
 * Event listener for HTTP server "error" event.
 */

function onError(error) {
  if (error.syscall !== 'listen') {
    throw error;
  }

  var bind = typeof port === 'string'
    ? 'Pipe ' + port
    : 'Port ' + port;

  // handle specific listen errors with friendly messages
  switch (error.code) {
    case 'EACCES':
      console.error(bind + ' requires elevated privileges');
      process.exit(1);
      break;
    case 'EADDRINUSE':
      console.error(bind + ' is already in use');
      process.exit(1);
      break;
    default:
      throw error;
  }
}

/**
 * Event listener for HTTP server "listening" event.
 */

function onListening() {
  var addr = server.address();
  var bind = typeof addr === 'string'
    ? 'pipe ' + addr
    : 'port ' + addr.port;
  flint.debug('Listening on ' + bind);
}


// gracefully shutdown (crtl-c)
process.on('SIGINT', function() {
  flint.debug('stopping...');
  server.close();
  flint.stop().then(function() {
    process.exit();
  });
});
