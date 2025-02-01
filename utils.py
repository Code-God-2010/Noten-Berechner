from main import app, db, Fach, Note, Muendliche_Note
def create_db():
    with app.app_context():
        db.create_all()

create_db()