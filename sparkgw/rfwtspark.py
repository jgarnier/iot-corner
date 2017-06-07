from flask import Flask, request, abort
# import the requests library so we can use it to make REST calls
import requests
import json
import time
import datetime
import urllib2


# disable warnings about using certificate verification
requests.packages.urllib3.disable_warnings()

app = Flask(__name__)


##-- Global state
myenv = [
          {"temp": {'init': False, "value": 0, "timestamp": 0}},
          {"redbutton": {'init': False, "value": 0, "timestamp": 0}},
        ]

##-- utils
def getenvbykey(keyname):
    localresult = None
    for oneenv in myenv:
        for onekey, onedata in oneenv.iteritems():
            if onekey == keyname:
               localresult = onedata
               break
    return localresult

def updateenvbykey(keyname, value):
    localresult = None
    localidx = 0
    for oneenv in myenv:
        for onekey, onedata in oneenv.iteritems():
            if onekey == keyname:
               myenv[localidx] = {keyname: {'init': True, "value": value, "timestamp": time.time()}}
               break
            localidx+=1
    print myenv
    return localresult

def getmessage(message_id):
    # login to developer.ciscospark.com and copy your access token here
    # Never hard-code access token in production environment
    token = 'Bearer ' + YOUR_BOT_TOKEN
    # add authorization to the header
    header = {"Authorization": "%s" % token}
    # create request url using message ID
    get_rooms_url = "https://api.ciscospark.com/v1/messages/" + message_id
    # send the GET request and do not verify SSL certificate for simplicity of this example
    api_response = requests.get(get_rooms_url, headers=header, verify=False)
    #print api_response.json()
    # parse the response in json
    response_json = api_response.json()
    # get the text value from the response
    text = response_json["text"]
    # return the text value
    return text

#Secret provided by
#  localtunnel.me
# ngrok http://www.lexev.org/en/2014/remote-url-localhost-server/
# https://stackoverflow.com/questions/34322988/view-random-ngrok-url-when-run-in-background
# https://developer.ciscospark.com/endpoint-webhooks-post.html
# MmQ3YTA0MGUtNGI1Zi00MTI3LTlmZTMtMjQxNGJhYmRjMTI0MzI2ZDFlYWYtYzhh

# curl -X POST -H "X-Device-Secret: 12345" http://localhost:8080/report?temp=32
# curl -X GET -H "X-Device-Secret: 12345" http://localhost:8080/local


YOUR_DEVICE_SECRET = "12345"
YOUR_BOT_TOKEN = ""
YOUR_ROOM_ID =  ""
YOUR_BOT_EMAIL =  ""
YOUR_BOT_EMAIL_ALIAS = YOUR_BOT_EMAIL.split('@')[0]
##-------------------------------------------
# Receive data from Arduino
@app.route('/report', methods =['POST'])
def inputFromArduino():
    headers = request.headers
    temperature = request.args.get('temp')
    incoming_secret = headers.get('X-Device-Secret')

    if temperature is None:
       abort(401)

    if incoming_secret is None:
       abort(401)

    elif YOUR_DEVICE_SECRET == incoming_secret:
        # we dont use it but for illustration
        json_file = request.json
        #toSpark('**Temperature:** '+temperature)
        updateenvbykey("temp",temperature)
        return 'Ok'
    else:
        print "Spoofed Hook"
        abort(401)

##-------------------------------------------
# Receive data from Arduino
@app.route('/local', methods =['GET'])
def readTemp():
    tempdata = getenvbykey("temp")
    print tempdata
    if tempdata['init'] == True:
        tmpdtstr = datetime.datetime.utcfromtimestamp(int(tempdata['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
        toSpark('Temperature: **'+tempdata['value']+ "** (last update: "+tmpdtstr+" GMT)")
    else:
        toSpark('**Temperature:** **ERROR** **Sensor is not initialised**')
    return 'Ok'

##-------------------------------------------
# webhook from spark
@app.route('/questions', methods =['POST'])
def inputFromSpark():
    # Get the json data
    json = request.json

    # parse the message id, person id, person email, and room id
    # ToDo: force constraints for json parsing - not required for demo
    message_id = json["data"]["id"]
    person_id = json["data"]["personId"]
    person_email = json["data"]["personEmail"]
    room_id = json["data"]["roomId"]

    # Could restrict message for a specific room

    # convert the message id into readable text
    message = getmessage(message_id)
    print(message)
    #print(YOUR_BOT_EMAIL_ALIAS+" TEMP?")
    message = message.split(YOUR_BOT_EMAIL_ALIAS)[1].lstrip(' ')
    if message == "TEMP?":
        tempdata = getenvbykey("temp")
        if tempdata['init'] == True:
           tmpdtstr = datetime.datetime.utcfromtimestamp(int(tempdata['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
           toSpark('Temperature: **'+tempdata['value']+ "** (last update: "+tmpdtstr+" GMT)")
        else:
           toSpark('**Temperature:** **ERROR** **Sensor is not initialised**')
    else:
        toSpark('I cant understand this question : *'+message+'*')
    return 'Ok'


##-------------------------------------------
# POST Function  that sends sometext in markdown to a Spark room
def toSpark(sometext):
    url = 'https://api.ciscospark.com/v1/messages'
    headers = {'accept':'application/json','Content-Type':'application/json','Authorization': 'Bearer ' + YOUR_BOT_TOKEN}
    values =   {'roomId': YOUR_ROOM_ID, 'markdown': sometext }
    data = json.dumps(values)
    req = urllib2.Request(url = url , data = data , headers = headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page


##-------------------------------------------
# main()
if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=8080, debug=True)
