from flask import Flask, request, abort
import json
import urllib2
from democonfig import *

app = Flask(__name__)


# curl -X POST -H "X-Device-Secret: 12345" 'http://localhost:8080/report?label=Temperature&key=temp&value=32'
# curl -X POST -H "X-Device-Secret: 12345" 'http://localhost:9090/report?label=BlueLed&key=led1&value=on'

@app.route('/report', methods =['POST'])

def inputArduino():
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
        toSpark('**'+alabel+':** '+avalue)
        return 'Ok'
    else:
        print "Spoofed Hook"
        abort(401)

@app.route('/report', methods =['GET'])
def inputArduinoGet():
    headers = request.headers
    alabel = request.args.get('label')
    akey = request.args.get('key')
    avalue = request.args.get('value')
    if  alabel is None or akey is None or avalue is None:
       abort(401)

    # we dont use it but for illustration
    json_file = request.json
    toSpark('**'+alabel+':** '+avalue)
    return 'Ok'

# POST Function  that sends the commits & comments in markdown to a Spark room
def toSpark(commits):
    url = 'https://api.ciscospark.com/v1/messages'
    headers = {'accept':'application/json','Content-Type':'application/json','Authorization': 'Bearer ' + YOUR_BOT_TOKEN}
    values =   {'roomId': YOUR_ROOM_ID, 'markdown': commits }
    data = json.dumps(values)
    req = urllib2.Request(url = url , data = data , headers = headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    return the_page

if __name__ == '__main__':
    app.run(host=YOUR_HOST_LISTENER , port=YOUR_LOCAL_PORT, debug=True)
