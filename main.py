from sqlite3 import Cursor
from flask import Flask
from flask import render_template
from pymongo import MongoClient
from flask_socketio import SocketIO,send
import time
from bson.json_util import dumps, loads
from pyparsing import col
import json
import ast

app = Flask(__name__,static_url_path='', 
            static_folder='static',)
app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)
socketio = SocketIO(app, cors_allowed_origins='*',async_mode='gevent')


client=MongoClient("mongodb+srv://maagauiya:loopcool@cluster0.f7uie.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=client['ruhavik_realtime']
collection=db['ruhavik']


@app.route("/")
def hello_world():



    collection=db['ruhavik']
    cursor = collection.find()
    collection=db['ruhavik_city']
    cursor2 = collection.find()
    

    return render_template('main.html', name=None, cars = cursor,cities = cursor2)

    
@socketio.on('message')
def handle_message(msg):
    collection=db['ruhavik']
    cursor = collection.find()
  
    cursor = json.loads(dumps(cursor))

    collection=db['ruhavik_city']
    cursor2 = collection.find()
    cursor2 = json.loads(dumps(cursor2))
    
    loop = { 
        'cursor':cursor,
        'cursor2' :cursor2
    }
    # print(    cursor[0])
    socketio.send(loop)

    time.sleep(1)


@socketio.on('op')
def handle_message(msg):
    print(msg)

if __name__ == "__main__":
    socketio.run(app)






