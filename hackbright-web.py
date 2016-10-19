from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def home():
    """Shows home page"""

    student_info = hackbright.show_all_students()
    project_info = hackbright.show_all_projects()
    print student_info, project_info
    return render_template("index.html", student_info=student_info, project_info=project_info)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github','jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    student_grades = hackbright.get_grades_by_github(github)
    html = render_template("student_info.html", first=first, last=last,
        github=github, student_grades=student_grades)
    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student"""

    return render_template("student_search.html")


@app.route("/student-add")
def student_add():
    """Displays form to add a new student"""

    return render_template("student_add.html")


@app.route("/student-added", methods=["POST"])
def student_added():
    """Adds a new student to the database and displays the confirmation"""

    github = request.form.get("github")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    hackbright.make_new_student(first_name,last_name,github)
    return render_template("student_add_success.html", first_name=first_name, 
        last_name=last_name, github=github)


@app.route("/project")
def show_project_info():
    """Displays the information associated with a specific project"""

    project = request.args.get('title', 'Markov')
    title, description, max_grade = hackbright.get_project_by_title(project)
    students_completed = hackbright.get_grades_by_title(project)
    return render_template("project_info.html", title=title, description=description,
        max_grade=max_grade, students_completed=students_completed)


@app.route("/project-add")
def project_add():
    """Displays form to add a new project"""
    
    return render_template("project_add.html")


@app.route("/project-added", methods=["POST"])
def project_added():
    """Adds a new project to the database and displays a confirmation"""
    
    title = request.form.get("title")
    desc = request.form.get("desc")
    max_grade = request.form.get("max_grade")
    hackbright.make_new_project(title, desc, max_grade)
    return render_template("project_add_success.html", title=title, desc=desc,
        max_grade=max_grade)


@app.route("/grade-add")
def grade_add():
    """Displays form to add/update grade for a student project using their github"""

    students = hackbright.show_all_students()
    projects = hackbright.show_all_projects()
    return render_template("grade_add.html", students=students, projects=projects)


@app.route("/grade-added")
def grade_added():
    pass


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
