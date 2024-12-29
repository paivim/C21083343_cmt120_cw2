from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages and CSRF protection

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional but recommended to silence warnings

# Initialize the database
db = SQLAlchemy(app)

# Define the Project model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID for each project
    title = db.Column(db.String(100), nullable=False)  # Project title
    description = db.Column(db.String(300), nullable=False)  # Project description
    link = db.Column(db.String(200), nullable=True)  # Optional link to the project

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID
    username = db.Column(db.String(50), nullable=False, unique=True)  # Username
    email = db.Column(db.String(120), nullable=False, unique=True)  # Email address
    password = db.Column(db.String(200), nullable=False)  # Hashed password

    def __repr__(self):
        return f'<User {self.username}>'

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

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
    projects = Project.query.all()  # Fetch all projects from the database
    return render_template('portfolio.html', projects=projects)

@app.route('/project/<int:project_id>')
def project_page(project_id):
    project = Project.query.get_or_404(project_id)
    print(f"Project ID: {project.id}, Title: {project.title}")
    return render_template('project.html', project=project)


@app.route('/debug_db')
def debug_db():
    projects = Project.query.all()
    return {
        "projects": [
            {
                "id": project.id,
                "title": project.title,
                "description": project.description,
                "link": project.link,
            }
            for project in projects
        ]
    }

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle the form submission
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))

        # Check if the username already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists!", "danger")
            return redirect(url_for('register'))

        # Check if the email already exists in the database
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("Email already exists!", "danger")
            return redirect(url_for('register'))

        # Hash the password before saving it
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Save the new user to the database
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful!", "success")
        return redirect(url_for('home'))

    return render_template('register.html')


@app.route('/send-message', methods=['POST'])
def send_message():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Log or process the message
    print(f"Message from {name} ({email}): {message}")

    # Flash success message
    flash("Your message has been sent successfully!", "success")
    
    # Redirect back to the contact page
    return redirect(url_for('contact'))





if __name__ == '__main__':
    app.run(debug=True)