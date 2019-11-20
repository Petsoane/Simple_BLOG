from flask import Flask
from flask_socketio import SocketIO, send, emit
from matcha.models import Database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secrete'
socket = SocketIO(app)
db = Database('match.db')
db.congfig()

from matcha import routes