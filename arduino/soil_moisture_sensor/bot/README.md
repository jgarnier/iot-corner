Soil Moisture Sensor Bot
========================

Spark Bot for the Soil Moisture Sensor.

It is based on the ["flint-bot"](https://github.com/flint-bot/flint) framework.


## Building the app

    $ npm install

## Running the app

    $ export SPARK_TOKEN="Tm90aGluZyB0b..."
    $ export SPARK_WEBHOOKURL="http://myserver.com/"
    $ SOILSENSOR_PORT=3001
    $ npm start

## Posting sensor measures

The bot receives new measures from the sensors using a POST on "http://myserver.com/soilmoisturesensor/:deviceId".

Have a try with following example:

    $ curl --data "moistureLevel=12" http://localhost:3001/soilmoisturesensor/12345


## References

[Spark API](https://spark.laravel.com/docs/3.0/api)
