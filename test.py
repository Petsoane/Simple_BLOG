from flask import Flask
from flaskext.mysql import MySQL
import cryptography

mysql = MySQL()
app = Flask(__name__)
app.config['SECRET'] = 'secret'
app.config['MYSQL_DATABASE_USER'] =  'root'
app.config['MYSQL_DATABASE_PASSWORD'] =  'Theophylus'
app.config['MYSQL_DATABASE_DB'] =  'test'
app.config['MYSQL_DATABASE_HOST'] =  'localhost'
app.config['MYSQL_DATABSE_PORT'] = 3306
mysql.init_app(app)

@app.route("/")
def hello():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('INSERT test(name, surname) VALUES ("LBO", "TEST")')
    conn.commit()
    return 'Yay! I think it works'


if __name__ == '__main__':
    app.run(debug=True)