#Python LED Web Handler
import socket
from json import dumps
from time import sleep

from flask import Flask, render_template, request
from flask_jsonpify import jsonify
from flask_restful import Api, Resource

from papirus import LM75B, PapirusTextPos

rot = 90
papirus_text = PapirusTextPos(False, rotation=rot)
ipAddr = socket.gethostname()
lines = [ipAddr, "", "", "", "", "", "", "", ""]
ids = ["One", "Two", "Three", "Four", "Five", \
	"Six", "Seven", "Eight", "Nine"]
app = Flask(__name__)
api = Api(app)

class set_text(Resource):
    def get(self, index, text):
        print("Index: "+index)
        print("Text: "+text)
        offset = int(index)-1
        print("offset: {}".format(offset))
        print("Testing: "+lines[0])
        lines[offset] = text
        print("Text: "+lines[offset])
        try:
            papirus_text.AddText( \
                lines[offset], 0, offset*14, Id=ids[offset], size=12)
        except:
            print("What the heck?")
        #text.WriteAll()
        #result = {'data':dict(zip(sz.value.StatusZeroValue))}
        return jsonify({'data':lines})

class clear_text(Resource):
    def get(self, index):
        print("Index: "+index)
        offset = int(index)-1
        print("offset: {}".format(offset))
        lines[offset] = ""
        papirus_text.AddText( \
            lines[offset], 0, offset*14, Id=ids[offset+1], size=12)
        #text.WriteAll()
        #result = {'data':dict(zip(sz.value.StatusZeroValue))}
        return jsonify({'data':lines})

class commit_text(Resource):
    def get(self, index):
        try:
            papirus_text.WriteAll()
        except:
            print("What the heck?")
        #result = {'data':dict(zip(sz.value.StatusZeroValue))}
        return jsonify({'data':lines})

class get_text(Resource):
    def get(self):
        return jsonify({'data':lines})

api.add_resource(get_text, "/status")
api.add_resource(set_text, '/<index>/<text>') #Dynamic route
api.add_resource(clear_text, '/<index>')
api.add_resource(commit_text, '/commit')

# Routes
@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    papirus_text.AddText(lines[0], 0, 0, Id=ids[0], size=12)
    papirus_text.WriteAll()
    app.run(host='0.0.0.0', port=5555)
