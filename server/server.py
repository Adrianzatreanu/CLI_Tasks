from flask import Flask, request
from flask_cors import CORS
from shutil import copyfile
import json
import os
import subprocess
from time import sleep

from sanitychecker import SanityChecker
from dbhandler import DbHandler

PATH_TO_SERVER="server/"
app = Flask(__name__)
CORS(app)

def check_login(username):
    # currently only checks for the username.
    # should actually use an authentication service
    okay = DbHandler.username_exists(username)

    if okay:
        containers_dir_path = PATH_TO_SERVER + "containers"
        if not os.path.exists(containers_dir_path):
            os.mkdir(containers_dir_path)
        user_dir_path = PATH_TO_SERVER + "containers/" + username
        if not os.path.exists(user_dir_path):
            os.mkdir(user_dir_path)
        vagrant_file_path = user_dir_path + "/Vagrantfile"
        if not os.path.exists(vagrant_file_path):
            copyfile(PATH_TO_SERVER + "Vagrantfile", vagrant_file_path)

        new_env = os.environ
        new_env["VAGRANT_CWD"] = user_dir_path
        p = subprocess.Popen(["vagrant", "destroy"], env=new_env, stdout=subprocess.PIPE)
        sleep(5)
        print("Destroyed")
        p = subprocess.Popen(["vagrant", "up"], env=new_env, stdout=subprocess.PIPE)
        print(p.communicate())
        print("Sleeping 7s")
        sleep(7)
        print("Done")
    return okay

def task_completed(username, task):
    # should run the script on the docker instance
    if task == "test_task":
        return True
    return False

def calculate_score(seconds):
    # eventually should use some custom formula for each task

    if seconds < 5:
        return 100

    if seconds > 100:
        return 0

    return 100 - seconds

@app.route('/login', methods=['POST'])
def login():
    if request.method != "POST":
        return json.dumps({"login": "Only POST is supported"})
    data = request.get_json(force=True)

    sanity_check_result = SanityChecker.perform_login_sanity_checks(data)
    if sanity_check_result != SanityChecker.OK:
        return json.dumps({"login": sanity_check_result})

    username = data["username"][0]
    if not check_login(username):
        return json.dumps({"login": "failed"})

    return json.dumps({"login": "success"})

@app.route('/list_topics', methods=['GET'])
def list_topics():
    if request.method != "GET":
        return json.dumps({"list_topics": "Only GET is supported"})

    topics = DbHandler.list_topics()

    return json.dumps({"list_topics": topics})

@app.route('/list_tasks', methods=['POST'])
def list_tasks():
    if request.method != "POST":
        return json.dumps({"list_tasks": "Only POST is supported"})

    data = request.get_json(force=True)

    sanity_check_result = SanityChecker.perform_list_tasks_sanity_checks(data)
    if sanity_check_result != SanityChecker.OK:
        return json.dumps({"list_tasks": sanity_check_result})

    topic = data["topic"]
    username = data["username"]

    tasks = DbHandler.get_tasks_and_scores(topic, username)

    return json.dumps({"list_tasks": tasks})

@app.route('/get_all_tasks', methods=['GET'])
def get_all_tasks():
    if request.method != "GET":
        return json.dumps({"get_all_tasks": "Only GET is supported"})

    return json.dumps({"get_all_tasks": DbHandler.get_all_tasks()})

@app.route('/get_task_desc', methods=['POST'])
def get_task_desc():
    if request.method != "POST":
        return json.dumps({"get_task_desc": "Only POST is supported"})

    data = request.get_json(force=True)

    sanity_check_result = SanityChecker.perform_get_task_desc_sanity_checks(data)
    if sanity_check_result != SanityChecker.OK:
        return json.dumps({"get_task_desc": sanity_check_result})

    task = data["task"]

    return json.dumps({"get_task_desc": DbHandler.get_task_desc(task)})


@app.route('/get_score_for_user', methods=['POST'])
def get_score_for_user():
    if request.method != "POST":
        return json.dumps({"get_score_for_user": "Only POST is supported"})

    data = request.get_json(force=True)

    sanity_check_result = SanityChecker.perform_get_score_for_user_sanity_checks(data)
    if sanity_check_result != SanityChecker.OK:
        return json.dumps({"get_score_for_user": sanity_check_result})

    username = data["username"]

    score = round(DbHandler.get_score_for_user(username), 2)

    return json.dumps({"get_score_for_user": score})


@app.route('/execute', methods=['POST'])
def execute():
    if request.method != "POST":
        return json.dumps({"execute": "Only POST is supported"})
    data = request.get_json(force=True)

    sanity_check_result = SanityChecker.perform_execute_sanity_checks(data)
    if sanity_check_result != SanityChecker.OK:
        return json.dumps({"execute": sanity_check_result})

    cmd = ' '.join(data["cmd"])
    username = data["username"]
    output = "Command is not supported."

    if cmd == "ls":
        output = "mkr.txt"

    return json.dumps({"execute": output})

@app.route('/check_task', methods=['POST'])
def check_task():
    if request.method != "POST":
        return json.dumps({"check_task": "Only POST is supported", "message": "Bad request sent (" + str(request.method + ").")})
    data = request.get_json(force=True)

    sanity_check_result = SanityChecker.perform_check_task_sanity_checks(data)
    if sanity_check_result != SanityChecker.OK:
        return json.dumps({"check_task": sanity_check_result, "message": "Bad fields sent to server."})

    username = data["username"]
    seconds = data["seconds"]
    task = data["task"]
    message = ""

    if not task_completed(username, task):
        message = "Task not completed."
        return json.dumps({"check_task": "success", "message": message})

    old_score = DbHandler.get_score(username, task)
    new_score = round(calculate_score(seconds), 2)

    if new_score > old_score:
        DbHandler.update_score(username, task, new_score)
        message = "Congrats. New score: " + str(new_score) + ". Old: " + str(old_score)
    else:
        message = "Task completed. Score not updated. New: " + str(new_score) + ". Old: " + str(old_score)

    return json.dumps({"check_task": "success", "message": message})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
