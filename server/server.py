from flask import Flask, request
from flask_cors import CORS
import json

from sanitychecker import SanityChecker
from dbhandler import DbHandler

app = Flask(__name__)
CORS(app)

def check_login(username):
    # currently only checks for the username.
    # should actually use an authentication service
    return DbHandler.username_exists(username)

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

@app.route('/get_score_for_user', methods=['POST'])
def get_score_for_user():
    if request.method != "POST":
        return json.dumps({"get_score_for_user": "Only POST is supported"})

    data = request.get_json(force=True)

    sanity_check_result = SanityChecker.perform_get_score_for_user_sanity_checks(data)
    if sanity_check_result != SanityChecker.OK:
        return json.dumps({"get_score_for_user": sanity_check_result})

    username = data["username"]

    score = DbHandler.get_score_for_user(username)

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
    print("Cmd is: " + str(cmd))

    if cmd == "ls":
        output = "a.txt\nb.txt\n"

    return json.dumps({"execute": output})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
