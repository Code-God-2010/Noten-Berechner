from flask_mysqldb import MySQL
import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv(r'C:\Users\linla\Documents\GitHub\Noten-Berechner\MySQL_variables.env')
app = Flask(__name__)

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

print(get_all_users())