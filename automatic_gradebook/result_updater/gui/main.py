from flask import Flask, render_template, redirect,  request, make_response, session, abort
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from vizual_system.db import *
app = Flask(__name__)


def main():
    app.run()


@app.route("/")
def start():
    return redirect("index")


@app.route("/index")
def index():
    # TODO: true render from db
    all = {}
    all["courses"] = [["Добавить курс", "add_course"],
                      ["Просмотр всех рабочих ведомостей", "look_all"],
                      ["Просмотр всех заданий", "look_all_tasks"],
                      ["Добавления нового задания", "add_task"],
                      ["Просмотр списка студентов по группам", "students_group"],
                      ["Добавления нового студента в заданную группу", "add_student"],
                      ["Просмотра интерфейса настроек", "settings"]]
    return render_template("course_list.html", **all)


@app.route("/add_course", methods=['GET', 'POST'])
def add_course():
    if request.method == "GET":
        return render_template("add_course_form.html")
    elif request.method == "POST":
        course_name = request.form["short_name"]
        course_nicename = request.form["nicename"]
        # stud_list = request.files["stud_list"]
        # if stud_list:
        #     stud_list.save("file.xlsx")
        add_data("discipline(discipline,nice_name)", (course_name, course_nicename))
        print(course_name, course_nicename)
        return redirect("index")
        # TODO: redirect to course settings

    else:
        return render_template("index")


@app.route("/look_all")
def look_all():
    if request.method == "GET":
        return render_template("look_all.html")


@app.route("/add_student", methods=['GET', 'POST'])
def add_student():
    if request.method == "GET":
        return render_template("add_student.html")
    elif request.method == "POST":
        stud_name = request.form["stud_name"]
        course_name = request.form["course_name"]
        add_data("student_mapping_scheme", (stud_name, course_name))
        print(stud_name, course_name)
        return redirect("index")


@app.route("/add_task", methods=['GET', 'POST'])
def add_task():
    all = {}
    all["check_sistems"] = ["one", "two", "three"]

    if request.method == "GET":
        return render_template("add_task.html", **all)
    elif request.method == "POST":
        name = request.form["short_name"]
        chosen_system = request.form["chosen_sistem"]
        print(name, chosen_system)
        return redirect("index")
    else:
        return render_template("add_task.html", **all)


@app.route("/look_all_tasks")
def all_tasks():
    return render_template("all_tasks.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/students_group")
def students_groups():
    return render_template("students_group.html")


if __name__ == '__main__':
    main()
