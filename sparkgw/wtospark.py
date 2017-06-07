from flask import Flask, request, abort
import json
import urllib2

app = Flask(__name__)

#Secret provided by
# fbabottemp99
# MmQ3YTA0MGUtNGI1Zi00MTI3LTlmZTMtMjQxNGJhYmRjMTI0MzI2ZDFlYWYtYzhh

# curl -X POST -H "X-Device-Secret: 12345" http://localhost:8080/report?temp=32


YOUR_DEVICE_SECRET = "12345"
YOUR_BOT_TOKEN = ""
YOUR_ROOM_ID =  ""

@app.route('/report', methods =['POST'])

def inputArduino():
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
        toSpark('**Temperature:** '+temperature)
        return 'Ok'
    else:
        print "Spoofed Hook"
        abort(401)


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
    app.run(host='0.0.0.0' , port=8080, debug=True)
