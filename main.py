from flask import Flask, request, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import sqlalchemy.exc
from werkzeug.security import check_password_hash, generate_password_hash
def hash_password(password):
    return generate_password_hash(password)

def check_password(hashedPassword, password):
    return check_password_hash(hashedPassword, password)

login_manager = LoginManager()
app = Flask(__name__)
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Fächer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'd7db8ae39e4a13a6a03f2f0e'
db = SQLAlchemy(app)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    fächer = db.relationship('Fach', backref = 'user', lazy = 'dynamic')

class Fach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
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

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)

@app.route('/', methods=['GET', 'POST'])
@app.route('/signup', methods=['POST', 'GET'])
def home():
    global current_id
    if len(request.form)>0:
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = hash_password(password)
        user = User(username=username, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            current_id = user.id
        except sqlalchemy.exc.IntegrityError:
            return render_template('signup.html', error='Benutzername wird bereits benutzt')
        return redirect('/signedin')
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    global current_id
    if len(request.form)>0:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password(user.password, password):
            current_id = user.id
            login_user(user)
            return redirect('/signedin')
        else:
            return render_template('login.html', error='Benutzername oder Passwort ist falsch')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/signedin', methods=['POST', 'GET'])
def signedin():
    noten = Note.query.all()
    beste_note = min([note.wert for note in noten]) if len(noten) > 0 else 0.0
    schlechteste_note = max([note.wert for note in noten]) if len(noten) > 0 else 0.0
    durchschnitt = sum([note.wert for note in noten])/len(noten) if len(noten) > 0 else 0.0
    muendliche_noten = Muendliche_Note.query.all()
    beste_muendliche_note = min([muendliche_note.wert for muendliche_note in muendliche_noten]) if len(muendliche_noten) > 0 else 0.0
    schlechteste_muendliche_note = max([muendliche_note.wert for muendliche_note in muendliche_noten]) if len(muendliche_noten) > 0 else 0.0
    durchschnitt_muendliche_note = sum([muendliche_note.wert for muendliche_note in muendliche_noten])/len(muendliche_noten) if len(muendliche_noten) > 0 else 0.0
    subjects = Fach.query.filter_by(user_id=current_id).all()
    return render_template('signedin.html', subjects=subjects, signedin=True, beste_note=beste_note, schlechteste_note=schlechteste_note, durchschnitt=durchschnitt, beste_muendliche_note=beste_muendliche_note, schlechteste_muendliche_note=schlechteste_muendliche_note, durchschnitt_muendliche_note=durchschnitt_muendliche_note)

@app.route('/fach_hinzufügen', methods=['POST', 'GET'])
def fächer():
    subjects = Fach.query.filter_by(user_id=current_id).all()
    if len(request.form)>0:
        name = request.form.get('name')
        fach = Fach(name=name, user_id=current_id)
        db.session.add(fach)
        db.session.commit()
        return redirect('/signedin')
    return render_template('fach_hinzufügen.html', subjects=subjects, fach_hinzufügen=True)

@app.route('/fach_uebersicht/<string:subject>')
def fach_uebersicht(subject):
    subjects = Fach.query.filter_by(user_id=current_id).all()
    subject_obj = Fach.query.filter_by(name=subject, user_id=current_id).first()
    noten = Note.query.filter_by(fach_id=subject_obj.id).all()
    muendliche_noten = Muendliche_Note.query.filter_by(fach_id=subject_obj.id).all()
    muendliche_noten_avg =  None
    noten_avg = None
    if len(noten)>0:
        noten_avg = sum([note.wert for note in noten]) / len(noten)
    if len(muendliche_noten)>0:
        muendliche_noten_avg = sum([muendliche_note.wert for muendliche_note in muendliche_noten]) / len(muendliche_noten)
    return render_template('fachuebersicht.html', fach_uebersicht=True, subjects=subjects, noten_avg=noten_avg, muendliche_noten_avg=muendliche_noten_avg, subject=subject_obj, noten=noten, muendliche_noten=muendliche_noten)

@app.route('/note_hinzufügen', methods=['POST', 'GET'])
def noten_hinzufügen():
    subjects = Fach.query.filter_by(user_id=current_id).all()
    if len(request.form)>0:
        subject = request.form.get('subject')
        grade = request.form.get('grade')
        fach_obj = Fach.query.filter_by(name=subject, user_id=current_id).first()
        if fach_obj:
            note = Note(wert=grade, fach_id=fach_obj.id)
            db.session.add(note)
            db.session.commit()
            return redirect(f'/fach_uebersicht/{subject}')
        else:
            return render_template('note_hinzufügen.html', note_hinzufügen=True, subjects=subjects, error='Kein Fach mit diesem Namen gefunden')
    return render_template('note_hinzufügen.html', note_hinzufügen=True, subjects=subjects)

@app.route('/muendliche_note_hinzufügen', methods=['POST', 'GET'])
def muendliche_noten_hinzufügen():
    subjects = Fach.query.filter_by(user_id=current_id).all()
    if len(request.form)>0:
        subject = request.form.get('subject')
        grade = request.form.get('grade')
        fach_obj = Fach.query.filter_by(name=subject, user_id=current_id).first()
        if fach_obj:
            muendliche_note = Muendliche_Note(wert=grade, fach_id=fach_obj.id)
            db.session.add(muendliche_note)
            db.session.commit()
            return redirect(f'/fach_uebersicht/{subject}')
        else:
            return render_template('muendliche_note_hinzufügen.html', muendliche_note_hinzufügen=True, subjects=subjects, error='Kein Fach mit diesem Namen gefunden')
    return render_template('muendliche_note_hinzufügen.html', muendliche_note_hinzufügen=True, subjects=subjects)

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    subjects = Fach.query.filter_by(user_id=current_id).all()
    if len(request.form)>0:
        captcha = request.form.get('captcha')
        if captcha == 'W68HP':
            noten = []
            muendliche_noten = []
            user = User.query.filter_by(id=current_id).first()
            fach = Fach.query.filter_by(user_id=user.id).all()
            for f in fach:
                noten.append(Note.query.filter_by(fach_id=f.id).all())
                muendliche_noten.append(Muendliche_Note.query.filter_by(fach_id=f.id).all())
            for note in noten:
                for n in note:
                    db.session.delete(n)
                    db.session.commit()
            for muendliche_note in muendliche_noten:
                for mn in muendliche_note:
                    db.session.delete(mn)
                    db.session.commit()
            for f in fach:
                db.session.delete(f)
                db.session.commit()
        return redirect('/signedin')
    return render_template('reset.html', reset=True, subjects=subjects)
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    subjects = Fach.query.filter_by(user_id=current_id).all()
    if len(request.form)>0:
        captcha = request.form.get('captcha')
        if captcha == 'W68HP':
            noten = []
            muendliche_noten = []
            user = User.query.filter_by(id=current_id).first()
            fach = Fach.query.filter_by(user_id=user.id).all()
            for f in fach:
                noten.append(Note.query.filter_by(fach_id=f.id).all())
                muendliche_noten.append(Muendliche_Note.query.filter_by(fach_id=f.id).all())
            for note in noten:
                for n in note:
                    db.session.delete(n)
                    db.session.commit()
            for muendliche_note in muendliche_noten:
                for mn in muendliche_note:
                    db.session.delete(mn)
                    db.session.commit()
            for f in fach:
                db.session.delete(f)
                db.session.commit()
            db.session.delete(user)
            db.session.commit()
        return redirect('/')
    return render_template('delete.html', delete=True, subjects=subjects)

@app.route('/zeugnisnote', methods=['GET', 'POST'])
def zeugnisnote():
    subjects = Fach.query.filter_by(user_id=current_id).all()
    if len(request.form)>0:
        fach = request.form.get('fach')
        muendlich = request.form.get('muendlich')
        user = User.query.filter_by(id=current_id).first()
        subject = Fach.query.filter_by(name=fach, user_id=user.id).first()
        if subject:
            if muendlich == 'True':
                muendliche_note = Muendliche_Note.query.filter_by(fach_id=subject.id).all()
                noten = Note.query.filter_by(fach_id=subject.id).all()
                if not muendliche_note:
                    return render_template('zeugnisnote.html', error='Keine muendlichen Noten vorhanden', zeugnisnote=True)
                if not noten:
                    return render_template('zeugnisnote.html', error='Keine schriftlichen Noten vorhanden', zeugnisnote=True)
                noten_durchschnitt = sum([temp.wert for temp in noten])/len(noten)
                muendlicher_durchschnitt = sum([temp.wert for temp in muendliche_note])/len(muendliche_note)
                muendlich_prozent = request.form.get('muendlich_prozent')
                zeugnis_note = (muendlicher_durchschnitt*int(muendlich_prozent)+noten_durchschnitt*(100-int(muendlich_prozent)))/100
                return render_template('zeugnisnote.html', note=zeugnis_note, zeugnisnote=True)
            else:
                noten = Note.query.filter_by(fach_id=subject.id).all()
                if noten:
                    zeugnis_note=sum([temp.wert for temp in noten])/len(noten)
                    return render_template('zeugnisnote.html', note=zeugnis_note, zeugnisnote=True)
                else:
                    return render_template('zeugnisnote.html', error='Keine schriftlichen Noten vorhanden', zeugnisnote=True) 
    return render_template('zeugnisnote.html', zeugnisnote=True, subjects=subjects)

if __name__ == '__main__':
    app.run(debug=True)
