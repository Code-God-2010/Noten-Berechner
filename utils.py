from main import app, db, Fach, Note, Muendliche_Note, User
def create_db():
    with app.app_context():
        db.create_all()
def add_subject(subject_name):
    with app.app_context():
        new_subject = Fach(name=subject_name, user_id=2)
        db.session.add(new_subject)
        db.session.commit()
        print(f"Subject created")

def add_note(subject_name, grade):
    with app.app_context():
        subject = Fach.query.filter_by(name=subject_name, user_id=2).first()
        if subject:
            note = Note(wert=grade, fach_id=subject.id, user_id=2)
            db.session.add(note)
            db.session.commit()
            print(f"Note added for {subject_name}")
        else:
            print(f"Subject {subject_name} not found")

def add_muendliche_note(subject_name, grade):
    with app.app_context():
        subject = Fach.query.filter_by(name=subject_name, user_id=2).first()
        if subject:
            muendliche_note = Muendliche_Note(wert=grade, fach_id=subject.id, user_id=2)
            db.session.add(muendliche_note)
            db.session.commit()
            print(f"Muendliche note added for {subject_name}")
        else:
            print(f"Subject {subject_name} not found")

for i in range(20):
    add_muendliche_note('Mathe', 1)