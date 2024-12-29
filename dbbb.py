from app import db, app  # Import `db` and `app` from your main app file

with app.app_context():
    db.create_all()
    print("Database tables created!")
