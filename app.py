
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required, LoginManager, UserMixin
from flask_migrate import Migrate
import secrets
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
os.makedirs(app.instance_path, exist_ok=True)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Models
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    link = db.Column(db.String(200), nullable=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Comment {self.id}>"

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print(f"Name: {name}, Email: {email}, Message: {message}")
        flash("Thank you for your message!", "success")
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/portfolio')
def portfolio():
    projects = Project.query.all()
    return render_template('portfolio.html', projects=projects)

@app.route('/project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def project_page(project_id):
    project = Project.query.get_or_404(project_id)
    comments = Comment.query.filter_by(project_id=project_id).all()

    if request.method == 'POST':
        content = request.form.get('content')
        try:
            new_comment = Comment(
                username=current_user.username,
                email=current_user.email,
                content=content,
                author_id=current_user.id,
                project_id=project.id
            )
            db.session.add(new_comment)
            db.session.commit()
            flash("Your comment has been added!", "success")
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            flash("An error occurred while submitting your comment.", "danger")

        return redirect(url_for('project_page', project_id=project.id))

    return render_template('project.html', project=project, comments=comments)

@app.route('/delete-comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    project_id = comment.project_id
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted successfully!", "success")
    return redirect(url_for('project_page', project_id=project_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Username already exists!", "danger")
        elif existing_email:
            flash("Email already exists!", "danger")
        elif len(username) < 2:
            flash("Username must be at least 2 characters long!", "danger")
        elif len(password) < 6:
            flash("Password must be at least 6 characters long!", "danger")
        elif len(email) < 5:
            flash("Email must be at least 5 characters long!", "danger")
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful!", "success")
            return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('portfolio'))
        else:
            flash("Invalid username or password.", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", "info")
    return redirect(url_for('login'))

@app.route('/send-message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    print(f"Message from {name} ({email}): {message}")
    flash("Your message has been sent successfully!", "success")
    return redirect(url_for('contact'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Tables created successfully!")
    app.run(host="0.0.0.0", port=8080, debug=True)


