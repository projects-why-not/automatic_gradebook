import sqlite3
import os.path


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "gradebook")
con = sqlite3.connect(db_path, check_same_thread=False)
cur = con.cursor()


def get_data(name_table, data):
    global cur
    return cur.execute(f"""SELECT {data} FROM {name_table}""").fetchall()


def add_data(name_table, data):
    global cur
    print(name_table, data)
    cur.execute(f"""INSERT INTO {name_table} VALUES {data}""")
    con.commit()

def get_id_checking_system(name_system):
    return f"""SELECT task.id WHERE task.short_name=={name_system}"""

def get_tasks():
    global cur
    return cur.execute(f"""
    SELECT task.task_id, discipline.short_name, check_system.short_name 
    FROM task 
    INNER JOIN discipline_task ON task.id == discipline_task.task_id
    INNER JOIN discipline ON discipline_task.discipline_id == discipline.id
    INNER JOIN check_system ON task.check_system_id == check_system.id
    """)


def add_password(nice_name, login, password):
    global cur
    id = cur.execute(f"""SELECT check_system.id FROM check_system WHERE check_system.nice_name == {nice_name}""").fetchone()
    print(nice_name, login, password)
    cur.execute(f"""
    INSERT INTO check_system_credentials(login, password, check_system_id) VALUES 
    ({login}, {password}, {id}""")
    con.commit()


def view_tasks():
    global cur
    return cur.execute(f"""SELECT * FROM discipline_task""").fetchall()


def add_task(data):
    add_data("discipline_task", data)
    con.commit()


def get_students_by_group(name_group):
    str_param = f"WHERE class_name={name_group}"
    return get_data("student_mapping_scheme", str_param)


def add_student(name, class_name):
    add_data("student_mapping_scheme", name, class_name)
    con.commit()

