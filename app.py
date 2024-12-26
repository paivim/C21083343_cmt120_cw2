from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Project model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID for each project
    title = db.Column(db.String(100), nullable=False)  # Project title
    description = db.Column(db.String(300), nullable=False)  # Project description
    link = db.Column(db.String(200), nullable=True)  # Optional link to the project

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
        return "Thank you for your message!"
    return render_template('contact.html')

@app.route('/portfolio')
def portfolio():
    projects = Project.query.all()  # Retrieve all projects from the database
    return render_template('portfolio.html', projects=projects)

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

if __name__ == '__main__':
    app.run(debug=True)
