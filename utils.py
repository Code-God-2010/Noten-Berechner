from main import app, db, Fach, Note, Muendliche_Note, User
def create_db():
    with app.app_context():
        db.create_all()
def add_subject(subject_name):
    with app.app_context():
        new_subject = Fach(name=subject_name, user_id=1)
        db.session.add(new_subject)
        db.session.commit()