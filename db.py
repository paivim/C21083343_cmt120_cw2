from app import db, app  # Make sure `db` and `app` are imported from your main app file

with app.app_context():
    db.create_all()
print("Database tables created!")
