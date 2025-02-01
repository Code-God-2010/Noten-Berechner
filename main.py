from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import sqlalchemy.exc
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Fächer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    fächer = db.relationship('Fach', backref = 'user', lazy = 'dynamic')

class Fach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    noten = db.relationship('Note', backref = 'fach', lazy = 'dynamic')
    muendliche_noten = db.relationship('Muendliche_Note', backref = 'fach', lazy = 'dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wert = db.Column(db.Integer, nullable=False)
    fach_id = db.Column(db.Integer, db.ForeignKey('fach.id'), nullable=False)

class Muendliche_Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wert = db.Column(db.Integer, nullable=False)
    fach_id = db.Column(db.Integer, db.ForeignKey('fach.id'), nullable=False)
@app.route('/', methods=['GET', 'POST'])
@app.route('/signup', methods=['POST', 'GET'])
def home():
    if len(request.form)>0:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username=username, password=password)
        try:
            db.session.add(user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return render_template('signup.html', error='Benutzername wird bereits benutzt')
        return redirect('/signedin')
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if len(request.form)>0:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return redirect('/signedin')
        else:
            return render_template('login.html', error='Benutzername oder Passwort ist falsch')
    return render_template('login.html')

@app.route('/signedin', methods=['POST', 'GET'])
def signedin():
    return render_template('signedin.html')
if __name__ == '__main__':
    app.run(debug=True)