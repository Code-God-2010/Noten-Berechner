from flask_mysqldb import MySQL
import os
from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv(r'C:\Users\linla\Documents\GitHub\Noten-Berechner\MySQL_variables.env')
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')

mysql = MySQL(app)

# Get all users from the User table

def get_all_users():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM User")
        users = cur.fetchall()
        cur.close()
        return users
class User:
    def __init__(self, data):
        self.id = data[0]
        self.username = data[1]
        self.password = data[2]

def get_user(id):
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM User WHERE id = %s", (id,))
        user = cur.fetchone()
        cur.close()
        return User(user)

def create_user(username, password):
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO User (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()

print(get_user(10000100000))