import sqlite3


con = sqlite3.connect("gradebook", check_same_thread=False)
cur = con.cursor()


def get_data(name_table):
    global cur
    return cur.execute(f"""SELECT * FROM {name_table}""").fetchall()


def add_data(name_table, data):
    global cur
    cur.execute(f"""INSERT {name_table} VALUES {data})""")


def view_tasks():
    global cur
    return cur.execute(f"""SELECT * FROM discipline_task""").fetchall()


def add_task(data):
    add_data("discipline_task", data)


def get_students_by_group(name_group):
    str_param = f"WHERE class_name={name_group}"
    return get_data("student_mapping_scheme", str_param)


def add_student(name, class_name):
    add_data("student_mapping_scheme", name, class_name)

