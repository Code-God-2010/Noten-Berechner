""" 
Protection against brute forcing
Content without login
1.
User Profile:
Implement a user profile page where users can view and edit their personal information, such as name, email, and password.
Add a feature to change the password securely.
2.
Subject Management:
Allow users to delete subjects they have added.
3.
Note Management:
Allow users to edit or delete notes they have added.
Implement a feature to sort notes by subject or grade.
Add a feature to filter notes by subject or grade range.
4.
UI Design:
Use a responsive design to ensure the application looks good on different devices.
Implement a clean and intuitive user interface with clear navigation and easy-to-understand instructions.
Use color schemes that are friendly and appealing to the eyes.
Add a feature to customize the appearance of the application, such as changing the font, background color, or layout.
7.
Security:
Implement a secure login system with password hashing and salting.
Add a feature to reset the password if the user forgets it.
Implement a feature to delete the user's account and all associated data.
8.
Data Validation:
Validate user inputs to ensure they are in the correct format and within the expected range.
Implement a feature to prevent users from entering invalid grades or subjects.
10.
Accessibility:
Ensure the application is accessible to users with disabilities by following WCAG (Web Content Accessibility Guidelines) standards.
Add a feature to adjust the font size and contrast for better readability.
Implement a feature to provide alternative text descriptions for images.
11.
Internationalization:
Add support for multiple languages, allowing users to switch between different languages for the application interface.
Implement a feature to display dates and times in the user's preferred format.
12.
Performance Optimization:
Optimize the database queries to improve the application's performance.
Implement caching mechanisms to reduce the number of database queries.
"""
from flask import Flask, request, render_template, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from graph import create_graph
from flask_caching import Cache
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
import MySQLdb
def hash_password(password):
    return generate_password_hash(password)

def check_password(hashedPassword, password):
    return check_password_hash(hashedPassword, password)

app = Flask(__name__)
load_dotenv(r'C:\Users\linla\Documents\GitHub\Noten-Berechner\MySQL_variables.env')
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(app)
mysql = MySQL(app)

class User:
    def __init__(self, data):
        self.id = data[0]
        self.username = data[1]
        self.password = data[2]

class Grade:
    def __init__(self, data):
        self.id = data[0]
        self.number = data[1]
        self.user_id = data[2]
        self.subject_id = data[3]

class Subject:
    def __init__(self, data):
        self.id = data[0]
        self.name = data[1]
        self.user_id = data[2]

def load_one_subject(user_id, name):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM subject WHERE name = %s AND user_id = %s", (name, user_id))
    subject = cursor.fetchone()
    cursor.close()
    if subject:
        return Subject(subject)
    else:
        return None
def load_subjects(id):
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM subject WHERE user_id = {id}")
    subjects = cursor.fetchall()
    cursor.close()
    try:
        subject_objs = [Subject(data) for data in subjects]
    except:
        return []
    return subject_objs

def load_grades(id):
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM grade WHERE user_id = {id}")
    grades = cursor.fetchall()
    cursor.close()
    try:
        grade_objs = [Grade(data) for data in grades]
    except:
        return []
    return grade_objs
def load_grades_for_subject(subject_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM grade WHERE subject_id = %s", (subject_id,))
    grades = cursor.fetchall()
    cursor.close()
    try:
        grade_objs = [Grade(data) for data in grades]
    except:
        return []
    return grade_objs
def load_oral_grades(id):
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM oral_grade WHERE user_id = {id}")
    oral_grades = cursor.fetchall()
    cursor.close()
    try:
        grade_objs = [Grade(data) for data in oral_grades]
    except:
        return []
    return grade_objs
def load_oral_grades_for_subject(subject_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM oral_grade WHERE subject_id = %s", (subject_id,))
    oral_grades = cursor.fetchall()
    cursor.close()
    try:
        grade_objs = [Grade(data) for data in oral_grades]
    except:
        return []
    return grade_objs

def load_user(id):
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM user WHERE id = {id}")
    user = cursor.fetchone()
    cursor.close()
    if user:
        return User(user)
    else:
        return None
@app.route('/', methods=['GET', 'POST'])
@app.route('/signup', methods=['POST', 'GET'])
def home():
    global current_id
    if len(request.form)>0:
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = hash_password(password)
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO User (username, password) VALUES (%s, %s)", (username, hashed_password))
            mysql.connection.commit()
            cur.close()
            cursor = mysql.connection.cursor()
            if username.isdigit():
                cursor.execute(f"SELECT * FROM user WHERE username = {username}".replace('"', ''))
            else:
                cursor.execute(f"SELECT * FROM user WHERE username = '{username}'")
            current_id = User(cursor.fetchone()).id
            cursor.close()
        except MySQLdb.IntegrityError:
            return render_template('signup.html', error='Benutzername wird bereits benutzt')
        return redirect('/signedin')
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    global current_id
    if len(request.form)>0:
        username = request.form.get('username')
        password = request.form.get('password')
        cursor = mysql.connection.cursor()
        if username.isdigit():
            cursor.execute(f"SELECT * FROM user WHERE username = {username}".replace('"', ''))
        else:
            cursor.execute(f"SELECT * FROM user WHERE username = '{username}'")
        user = cursor.fetchone()
        cursor.close()
        try:
            user = User(user)
        except:
            return render_template('login.html', error='Benutzername oder Passwort ist falsch')
        if user and check_password(user.password, password):
            current_id = user.id
            return redirect('/signedin')
        else:
            return render_template('login.html', error='Benutzername oder Passwort ist falsch')
    return render_template('login.html')

@app.route('/logout')
def logout():
    cache.clear()
    return redirect('/')

@app.route('/signedin', methods=['POST', 'GET'])
def signedin():
    noten = load_grades(current_id)
    beste_note = min([note.number for note in noten]) if len(noten) > 0 else 0.0
    schlechteste_note = max([note.number for note in noten]) if len(noten) > 0 else 0.0
    durchschnitt = sum([note.number for note in noten])/len(noten) if len(noten) > 0 else 0.0
    muendliche_noten = load_oral_grades(current_id)
    beste_muendliche_note = min([muendliche_note.number for muendliche_note in muendliche_noten]) if len(muendliche_noten) > 0 else 0.0
    schlechteste_muendliche_note = max([muendliche_note.number for muendliche_note in muendliche_noten]) if len(muendliche_noten) > 0 else 0.0
    durchschnitt_muendliche_note = sum([muendliche_note.number for muendliche_note in muendliche_noten])/len(muendliche_noten) if len(muendliche_noten) > 0 else 0.0
    subjects = load_subjects(current_id)
    return render_template('signedin.html', subjects=subjects, signedin=True, beste_note=beste_note, schlechteste_note=schlechteste_note, durchschnitt=durchschnitt, beste_muendliche_note=beste_muendliche_note, schlechteste_muendliche_note=schlechteste_muendliche_note, durchschnitt_muendliche_note=durchschnitt_muendliche_note)

@app.route('/fach_hinzufügen', methods=['POST', 'GET'])
def fach_hinzufügen():
    subjects = load_subjects(current_id)
    if len(request.form)>0:
        name = request.form.get('name')
        if not name in [subject for subject in subjects]:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO subject (name, user_id) VALUES (%s, %s)", (name, current_id))
            mysql.connection.commit()
            cursor.close()
            return redirect('/signedin')
        return render_template('fach_hinzufügen.html', subjects=subjects, fach_hinzufügen=True, error='Fach existiert bereits')
    return render_template('fach_hinzufügen.html', subjects=subjects, fach_hinzufügen=True)

@app.route('/fach_uebersicht/<string:subject>')
def fach_uebersicht(subject):
    subjects = load_subjects(current_id)
    subject_obj = load_one_subject(current_id, subject)
    noten = load_grades_for_subject(subject_obj.id)
    muendliche_noten = load_oral_grades_for_subject(subject_obj.id)
    muendliche_noten_avg =  None
    noten_avg = None
    if len(noten)>0:
        noten_avg = sum([note.number for note in noten]) / len(noten)
    if len(muendliche_noten)>0:
        muendliche_noten_avg = sum([muendliche_note.number for muendliche_note in muendliche_noten]) / len(muendliche_noten)
    return render_template('fachuebersicht.html', fach_uebersicht=True, subjects=subjects, noten_avg=noten_avg, muendliche_noten_avg=muendliche_noten_avg, subject=subject_obj, noten=noten, muendliche_noten=muendliche_noten)

@app.route('/note_hinzufügen', methods=['POST', 'GET'])
def noten_hinzufügen():
    subjects = load_subjects(current_id)
    if len(request.form)>0:
        subject = request.form.get('subject')
        grade = request.form.get('grade')
        fach_obj = load_one_subject(current_id, subject)
        if fach_obj:
            cursor = mysql.connection.cursor()
            cursor.execute(f'INSERT INTO grade(number, user_id, subject_id) VALUES ({grade}, {current_id}, {fach_obj.id})')
            mysql.connection.commit()
            cursor.close()
            return redirect(f'/fach_uebersicht/{subject}')
        else:
            return render_template('note_hinzufügen.html', note_hinzufügen=True, subjects=subjects, error='Kein Fach mit diesem Namen gefunden')
    return render_template('note_hinzufügen.html', note_hinzufügen=True, subjects=subjects)

@app.route('/muendliche_note_hinzufügen', methods=['POST', 'GET'])
def muendliche_noten_hinzufügen():
    subjects = load_subjects(current_id)
    if len(request.form)>0:
        subject = request.form.get('subject')
        grade = request.form.get('grade')
        fach_obj = load_one_subject(current_id, subject)
        if fach_obj:
            cursor = mysql.connection.cursor()
            cursor.execute(f'INSERT INTO oral_grade(number, user_id, subject_id) VALUES ({grade}, {current_id}, {fach_obj.id})')
            mysql.connection.commit()
            cursor.close()
            return redirect(f'/fach_uebersicht/{subject}')
        else:
            return render_template('muendliche_note_hinzufügen.html', muendliche_note_hinzufügen=True, subjects=subjects, error='Kein Fach mit diesem Namen gefunden')
    return render_template('muendliche_note_hinzufügen.html', muendliche_note_hinzufügen=True, subjects=subjects)

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    subjects = load_subjects(current_id)
    if len(request.form)>0:
        captcha = request.form.get('captcha')
        if captcha == 'W68HP':
            noten = []
            muendliche_noten = []
            fach = subjects
            for f in fach:
                noten.append(load_grades_for_subject(f.id))
                muendliche_noten.append(load_oral_grades_for_subject(f.id))
            for note in noten:
                for n in note:
                    cursor = mysql.connection.cursor()
                    cursor.execute(f"DELETE FROM grade WHERE id={n.id}")
                    mysql.connection.commit()
                    cursor.close()
            for muendliche_note in muendliche_noten:
                for mn in muendliche_note:
                    cursor = mysql.connection.cursor()
                    cursor.execute(f"DELETE FROM oral_grade WHERE id={mn.id}")
                    mysql.connection.commit()
                    cursor.close()
            for f in fach:
                cursor = mysql.connection.cursor()
                cursor.execute(f"DELETE FROM subject WHERE id={f.id}")
                mysql.connection.commit()
                cursor.close()
        return redirect('/signedin')
    return render_template('reset.html', reset=True, subjects=subjects)
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    subjects = load_subjects(current_id)
    if len(request.form)>0:
        captcha = request.form.get('captcha')
        if captcha == 'W68HP':
            noten = []
            muendliche_noten = []
            user = load_user(current_id)
            fach = load_subjects(current_id)
            for f in fach:
                noten.append(load_grades(current_id))
                muendliche_noten.append(load_oral_grades(current_id))
            for note in noten:
                for n in note:
                    cursor = mysql.connection.cursor()
                    cursor.execute(f"DELETE FROM grade WHERE id={n.id}")
                    mysql.connection.commit()
                    cursor.close()
            for muendliche_note in muendliche_noten:
                for mn in muendliche_note:
                    cursor = mysql.connection.cursor()
                    cursor.execute(f"DELETE FROM oral_grade WHERE id={mn.id}")
                    mysql.connection.commit()
                    cursor.close()
            for f in fach:
                cursor = mysql.connection.cursor()
                cursor.execute(f"DELETE FROM subject WHERE id={f.id}")
                mysql.connection.commit()
                cursor.close()
            cursor = mysql.connection.cursor()
            cursor.execute(f"DELETE FROM user WHERE id={current_id}")
            mysql.connection.commit()
            cursor.close()
        cache.clear()
        return redirect('/')
    return render_template('delete.html', delete=True, subjects=subjects)

@app.route('/zeugnisnote', methods=['GET', 'POST'])
def zeugnisnote():
    subjects = load_subjects(current_id)
    if len(request.form)>0:
        fach = request.form.get('fach')
        muendlich = request.form.get('muendlich')
        user = load_user(current_id)
        subject = load_one_subject(current_id, fach)
        if subject:
            if muendlich == 'True':
                muendliche_note = load_oral_grades_for_subject(subject.id)
                noten = load_grades_for_subject(subject.id)
                if not muendliche_note:
                    return render_template('zeugnisnote.html', subjects=subjects, error='Keine muendlichen Noten vorhanden', zeugnisnote=True)
                if not noten:
                    return render_template('zeugnisnote.html', subjects=subjects, error='Keine schriftlichen Noten vorhanden', zeugnisnote=True)
                noten_durchschnitt = sum([temp.number for temp in noten])/len(noten)
                muendlicher_durchschnitt = sum([temp.number for temp in muendliche_note])/len(muendliche_note)
                muendlich_prozent = request.form.get('muendlich_prozent')
                zeugnis_note = (muendlicher_durchschnitt*int(muendlich_prozent)+noten_durchschnitt*(100-int(muendlich_prozent)))/100
                return render_template('zeugnisnote.html', subjects=subjects, note=zeugnis_note, zeugnisnote=True)
            else:
                noten = load_grades_for_subject(subject.id)
                if noten:
                    zeugnis_note=sum([temp.number for temp in noten])/len(noten)
                    return render_template('zeugnisnote.html', subjects=subjects, note=zeugnis_note, zeugnisnote=True)
                else:
                    return render_template('zeugnisnote.html', subjects=subjects, error='Keine schriftlichen Noten vorhanden', zeugnisnote=True)
        else:
            return render_template('zeugnisnote.html', subjects=subjects, error='Kein Fach mit diesem Namen gefunden', zeugnisnote=True)
    return render_template('zeugnisnote.html', zeugnisnote=True, subjects=subjects)

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    subjects = load_subjects(current_id)
    noten = load_grades(current_id)
    create_graph([note.number for note in noten])
    return render_template('graph.html', graph=True, subjects=subjects)

if __name__ == '__main__':
    app.run(debug=True)
