from flask import Flask
from flask_socketio import SocketIO, send, emit
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)


app.config['SECRET_KEY'] = 'secrete'
app.config['UPLOAD_FOLDER'] = app.root_path + '/static/profile_pics'
app.config['SECRET'] = 'secret'
app.config['MYSQL_DATABASE_USER'] =  'root'
app.config['MYSQL_DATABASE_PASSWORD'] =  'Theophylus'
app.config['MYSQL_DATABASE_DB'] =  'Matcha'
app.config['MYSQL_DATABASE_HOST'] =  'localhost'
app.config['MYSQL_DATABSE_PORT'] = 3306


socket = SocketIO(app)
mysql.init_app(app)


from matcha.models import Database
db = Database('match.db')
db.congfig()

from matcha import routes