#Python LED Web Handler
import socket

from flask import Flask, render_template
from flask_jsonpify import jsonify
from flask_restful import Api, Resource

from papirus import PapirusTextPos

rot = 90
papirus_text = PapirusTextPos(False, rotation=rot)
ipAddr = socket.gethostname()
lines = [ipAddr, "", "", "", "", "", "", "", ""]
ids = ["One", "Two", "Three", "Four", "Five",
    "Six", "Seven", "Eight", "Nine"]
app = Flask(__name__)
api = Api(app)


class set_text(Resource):
    def get(self, index, text):
        print("Index: " + index)
        print("Text: " + text)
        offset = int(index) - 1
        print("offset: {}".format(offset))
        print("Testing: " + lines[0])
        lines[offset] = text
        print("Text: " + lines[offset])
        return jsonify({'data': lines})


class clear_text(Resource):
    def get(self, index):
        print("Index: " + index)
        offset = int(index) - 1
        print("offset: {}".format(offset))
        lines[offset] = ""
        return jsonify({'data': lines})

class get_text(Resource):
    def get(self):
        return jsonify({'data': lines})


class commit_text(Resource):
    def get(self):
        for i in range(0,9):
            papirus_text.UpdateText(ids[i], lines[i])
        papirus_text.WriteAll()
        return jsonify({'data':lines})

    
api.add_resource(get_text, "/status")
api.add_resource(set_text, '/<index>/<text>')  # Dynamic route
api.add_resource(clear_text, '/<index>/')
api.add_resource(commit_text, '/commit/')


# Routes
@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    for i in range(0, 9):
        papirus_text.AddText(lines[i], 0, i*14, Id=ids[i], size=12)
    papirus_text.WriteAll()
    app.run(host='0.0.0.0', port=5555)
