from flask import Flask, render_template, redirect,  request, make_response, session, abort
from vizual_system.db import *
app = Flask(__name__)


def main():
    # add_data("check_system(nice_name,short_name)", ("Яндекс контест", "Янд. контест"))
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

        add_data("discipline(short_name,nice_name)", (course_name, course_nicename))
        print(course_name, course_nicename)
        return redirect("index")
        # TODO: redirect to course settings

    else:
        return render_template("index")


@app.route("/look_all")
def look_all():
    data = get_data("discipline", "short_name, nice_name, form_path, student_mapping_path")
    return render_template("look_all.html", data=data)


@app.route("/add_student", methods=['GET', 'POST'])
def add_student():
    if request.method == "GET":
        return render_template("add_student.html")
    elif request.method == "POST":
        stud_name = request.form["stud_name"]
        course_name = request.form["course_name"]
        add_data("student_mapping_scheme(name,class_name)", (stud_name, course_name))
        return redirect("index")


@app.route("/add_task", methods=['GET', 'POST'])
def add_task():
    all = {}
    # all["check_sistems"] = list(get_data("check_system", ))
    all["data"] = get_data("check_system", "short_name")
    print(all["data"])
    if request.method == "GET":
        return render_template("add_task.html", **all)
    elif request.method == "POST":
        name = request.form["short_name"]
        chosen_system = request.form["chosen_sistem"]
        chosen_system_id = get_data("check_system", "id")
        add_data("task(task_id,check_system_id)", (name, chosen_system))
        print(name, chosen_system)
        return redirect("index")
    else:
        return render_template("add_task.html", **all)


@app.route("/look_all_tasks")
def all_tasks():
    data = get_tasks()
    return render_template("all_tasks.html", data=data)


@app.route("/settings", methods=["POST", "GET"])
def settings():
    data = get_data("check_system", "nice_name")
    if request.method == "GET":
        return render_template("settings.html", data=data)
    elif request.method == "POST":
        for item in data:
            print("!!!")
            login = request.form[f"system_{item}_login"]
            password = request.form[f"system_{item}_password"]
            add_password(item, login, password)
        return redirect("index")


@app.route("/students_group")
def students_groups():
    data = list(get_data("student_mapping_scheme", "class_name,name"))
    data.sort(key=lambda x: x[1])
    print(data)
    return render_template("students_group.html", data=data)


if __name__ == '__main__':
    main()
