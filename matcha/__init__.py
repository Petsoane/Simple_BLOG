from flask import Flask
from flask_socketio import SocketIO, send, emit
from matcha.models import Database

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secrete'
app.config['UPLOAD_FOLDER'] = app.root_path + '/static/profile_pics'
socket = SocketIO(app)
db = Database('match.db')
db.congfig()

from matcha import routes