from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def home():
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
    """Add a student"""

    return render_template("student_add.html")

@app.route("/student-added", methods=["POST"])
def student_added():

    github = request.form.get("github")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    hackbright.make_new_student(first_name,last_name,github)
    return render_template("student_add_success.html", first_name=first_name, 
        last_name=last_name, github=github)

@app.route("/project")
def show_project_info():

    project = request.args.get('title', 'Markov')
    title, description, max_grade = hackbright.get_project_by_title(project)
    students_completed = hackbright.get_grades_by_title(project)
    return render_template("project_info.html", title=title, description=description,
        max_grade=max_grade, students_completed=students_completed)



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
