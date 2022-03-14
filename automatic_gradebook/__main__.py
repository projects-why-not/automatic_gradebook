# coding=utf-8
from result_updater.data.form_params import *
from result_updater.checking_system.system import *

from result_updater.form_backend import Gradebook, GSheetsBackend, ExcelBackend
from result_updater.form_backend.google_sheets.authorization import Authorizer

from result_updater.utils.path_constants import *
from result_updater.student_list import CSVStudentList

import os
import json


def print_updates(updates):
    print("ОБНОВЛЕНИЯ:")
    for course_name in updates.keys():
        print(course_name)
        for student in updates[course_name].keys():
            print("\t{}:".format(student))
            for upd in updates[course_name][student]:
                print("\t\t", upd)


self_dir = os.path.dirname(os.path.abspath(__file__))

form_paths = {
    "qwerty": "qwe.xlsx"
}

if __name__ == "__main__":
    updates = {}

    authorizers = []
    for course_name in form_paths:
        authorizers += [block["system"] for block in get_params(course_name)["blocks"]]
    authorizers = set(authorizers)
    authorizers = {k: get_authorizer(k) for k in authorizers}

    sessions = {}
    for k,v in authorizers.items():
        sessions[k] = v.get_session()

    for course_name in form_paths.keys():
        form_params = get_params(course_name)

        updater = Gradebook(form_paths[course_name],
                            form_params["blocks"],
                            CSVStudentList(self_dir + STUDENT_MAPPING_DIR_REL_PATH + form_params["mapping_file"]),
                            ExcelBackend())

        for block in form_params["blocks"]:
            system_name = block["system"]
            fetcher = get_fetcher_class(system_name)(sessions[system_name],
                                                     block["tasks"],
                                                     block["check_type"],
                                                     self_dir + UPDATE_DIR_REL_PATH + course_name + "_" + system_name + "_{}_updates.csv")
            filenames = fetcher.fetch_updates()
            updater.add_updates(filenames,
                                block)
        form_paths[course_name] = updater.save()

    # TODO: logout at authorizers
