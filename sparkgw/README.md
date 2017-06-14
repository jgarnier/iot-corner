# sparkgw (Spark Gateway)

## Prerequisite

Before using the Spark Gateway, you need to install python packages by running:
```
sudo pip2 install -r requirements.txt
```

## wtospark.py (write to spark)

Basic Python sample code for receiving data from Arduino and writing to a spark room.

By default, it listens on 0.0.0.0:8080. Edit the file democonfig.py for setting any other values.

''curl -X POST -H "X-Device-Secret: 12345" http://localhost:8080/report?temp=32''

You should go to [Cisco Spark for Developers](https://developer.ciscospark.com), login, then register your first bot.
You can then create a room, either via API or via one of the spark client.
On the spark web site, if you activate the test mode, you can play with queries live.

In the python script democonfig.py, you should fill the following variables with the proper value:
  - YOUR_BOT_TOKEN = ""
  - YOUR_ROOM_ID =  ""
  - YOUR_BOT_EMAIL =  ""

Note: your bot email is mybot@spark.io if you named it mybot.

Each time you send a POST to the server, it will write "Temperature: 32" in your spark room.


## Spark and webhook

If you are running the python script locally on a laptop, the server needs to receive incoming request on a well defined
URL.

For doing so, you can use a tunnel to your localhost with solution such as ngrok (https://ngrok.com/).

Download ngrok for your distribution, unzip it and then start ./ngrok http 8080.

The returned URL is valid as long as ngrok is running (free version). Each time you close ngrok, a new URL will be built
and you will have to renew the webhook update.


## rfwtospark.py (read from and write to spark)

Basic Python sample code for receiving data from Arduino and writing to a spark room.
But this script can also receive messages from your spark room.

You should have done the first test with wtospark.py.

On the spark web site, go to https://developer.ciscospark.com/endpoint-webhooks-post.html, and create your callback.

Let's do a first callback with the following parameters:
  - name: tempwebhook
  - targetUrl: see previous section
  - resources: messages
  - event: created
  - filter: mentionedPeople=thisIsYourBotId

thisIsYourBotId should be replaced by the spark Id of your bot. This looks like a long string such as GFyazovL3VzL1BFT....GFyazovL3VzL1BFT.

In the python script democonfig.py, you should fill the following variables with the proper value:
  - YOUR_BOT_TOKEN = ""
  - YOUR_ROOM_ID =  ""
  - YOUR_BOT_EMAIL =  ""

Note: your bot email is mybot@spark.io if you named it mybot.

You can now send order from the spark room to your server œmybot.

Let's go with examples:

If your Arduino is sending the following events:
  - curl -X POST -H "X-Device-Secret: 12345" 'http://localhost:8080/report?label=Temperature&key=temp&value=32'
  - curl -X POST -H "X-Device-Secret: 12345" 'http://localhost:8080/report?label=BlueLed&key=led1&value=on'

From the spark room, you can post the following command:
  - @mybot GET temp
  - @mybot GET led1

Once your Arduino has started to send event such as label / key / value, you can send SET commands from your spark room:
  - @mybot SET temp 23
  - @mybot SET led1 off

The python server stores the state for each key/value pair reporter by the Arduino (states are lost on server stop).

The Arduino can pull any pending order for a given key by doing:
  - curl -X GET -H "X-Device-Secret: 12345" http://localhost:8080/getcmdbykey?key=temp
  - curl -X GET -H "X-Device-Secret: 12345" http://localhost:8080/getcmdbykey?key=led1
