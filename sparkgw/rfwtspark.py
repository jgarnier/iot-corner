from flask import Flask, request, abort
# import the requests library so we can use it to make REST calls
import requests
import json
import time
import datetime
import urllib2
from democonfig import *

# disable warnings about using certificate verification
requests.packages.urllib3.disable_warnings()

app = Flask(__name__)

# Arduino commands
# curl -X POST -H "X-Device-Secret: 12345" 'http://localhost:9090/report?label=Temperature&key=temp&value=32'
# curl -X POST -H "X-Device-Secret: 12345" 'http://localhost:9090/report?label=BlueLed&key=led1&value=on'

# Read key value from this server
# curl -X GET -H "X-Device-Secret: 12345" http://localhost:9090/getcmdbykey?key=temp
# curl -X GET -H "X-Device-Secret: 12345" http://localhost:9090/getvaluebykey?key=temp

##-- Global state
myenv = [
          {"temp": {'init': False, "label":"", "value": "0", "command": "", "timestamp": 0}},
        ]

YOUR_BOT_EMAIL_ALIAS = YOUR_BOT_EMAIL.split('@')[0]

##-- utils
def getenvbykey(keyname):
    localresult = None
    for oneenv in myenv:
        for onekey, onedata in oneenv.iteritems():
            if onekey == keyname:
               localresult = onedata
               break
    return localresult

def updateenvbykey(keyname, label, value, command=""):
    localresult = None
    localidx = 0
    keyfound = False
    for oneenv in myenv:
        for onekey, onedata in oneenv.iteritems():
            if onekey == keyname:
               myenv[localidx] = {keyname: {'init': True, "label": label, "value": value, "command": command, "timestamp": time.time()}}
               break
            localidx+=1
    if keyfound == False:
        myenv.append({keyname: {'init': True, "label": label, "value": value, "command": command, "timestamp": time.time()}})
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


##-------------------------------------------
# Receive data from Arduino
@app.route('/report', methods =['POST'])
def inputFromArduino():
    headers = request.headers
    alabel = request.args.get('label')
    akey = request.args.get('key')
    avalue = request.args.get('value')
    incoming_secret = headers.get('X-Device-Secret')
    if incoming_secret is None or alabel is None or akey is None or avalue is None:
       abort(401)
    if YOUR_DEVICE_SECRET == incoming_secret:
        # we dont use it but for illustration
        json_file = request.json
        updateenvbykey(akey,alabel,avalue)
        return 'Ok'
    else:
        print "Spoofed Hook"
        abort(401)

##-------------------------------------------
# Receive req from Arduino to get a key value
@app.route('/getcmdbykey', methods =['GET'])
def readCommandByKey():
    headers = request.headers
    incoming_secret = headers.get('X-Device-Secret')
    akey = request.args.get('key')
    if incoming_secret is None or akey is None:
       abort(401)
    tempdata = getenvbykey(akey)
    if tempdata is None:
        abort(404)
    print tempdata
    if tempdata['init'] == True:
        ## Reset the order to empty string
        updateenvbykey(akey,tempdata['label'],tempdata['value'],"")
        return tempdata['command']
    return 'Ko'

##-------------------------------------------
# Receive req from Arduino to get a key value
@app.route('/getvaluebykey', methods =['GET'])
def readValueByKey():
    headers = request.headers
    akey = request.args.get('key')
    incoming_secret = headers.get('X-Device-Secret')
    if incoming_secret is None or akey is None:
       abort(401)
    tempdata = getenvbykey(akey)
    if tempdata is None:
        abort(404)
    print tempdata
    if tempdata['init'] == True:
        return tempdata['value']
    return 'Ko'

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
    sparkcmd = message.split(' ')
    if len(sparkcmd) < 2 and len(sparkcmd) > 3:
        toSpark('I cant understand your request : *'+message+'*')
        return 'Ko'
    sparkorder=sparkcmd[0].lstrip(' ')
    sparkkey=sparkcmd[1].lstrip(' ')

    tempdata = getenvbykey(sparkkey)

    if tempdata is None:
        toSpark('I cant find a sensor with the id : *'+sparkkey+'*')
        return 'Ko'

    if sparkorder == "GET":

        if tempdata['init'] == True:
           tmpdtstr = datetime.datetime.utcfromtimestamp(int(tempdata['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')
           toSpark(tempdata['label']+': **'+tempdata['value']+ "** (last update: "+tmpdtstr+" GMT)")
        else:
           toSpark('**'+tempdata['label']+':** **ERROR** **Sensor has not yet reported values**')
    elif sparkorder == "SET"and len(sparkcmd) == 3:
        tempdata = getenvbykey(sparkkey)
        sparkcmd=sparkcmd[2].lstrip(' ')
        if tempdata['init'] == True:
           updateenvbykey(sparkkey,tempdata['label'],tempdata['value'],sparkcmd)
           toSpark('The **'+tempdata['label']+':** will be set to '+sparkcmd+' soon')
        else:
           toSpark('**'+tempdata['label']+':** **ERROR** **Sensor has not yet reported values**')
    else:
        toSpark('I cant understand your request : *'+message+'*')
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
    app.run(host=YOUR_HOST_LISTENER , port=YOUR_LOCAL_PORT, debug=True)
