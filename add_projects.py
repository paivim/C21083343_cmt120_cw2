from app import app, db, Project

with app.app_context():
    # Create sample projects
    project1 = Project(
        title="Dynamic Portfolio Website",
        description="A personal portfolio website showcasing skills and projects.",
        link="https://github.com/example-portfolio"
    )
    project2 = Project(
        title="Weather Forecast App",
        description="A web application that displays weather data for any city.",
        link="https://github.com/example-weather-app"
    )
    project3 = Project(
        title="E-commerce Website",
        description="An online platform for purchasing products.",
        link=None
    )

    # Add projects to the database
    db.session.add(project1)
    db.session.add(project2)
    db.session.add(project3)
    db.session.commit()  # Save changes


