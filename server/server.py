from flask import Flask, request
from flask_cors import CORS
import json

from sanitychecker import SanityChecker

app = Flask(__name__)
CORS(app)

def check_login(username):
    return True

@app.route('/login', methods=['POST'])
def login():
    if request.method != "POST":
        return json.dumps({"login": "Only POST is supported"})
    data = request.get_json(force=True)

    sanity_check_result = SanityChecker.perform_login_sanity_checks(data)
    if sanity_check_result != SanityChecker.OK:
        return json.dumps({"login": sanity_check_result})

    username = data["username"]
    if not check_login(username):
        return json.dumps({"login": "failed"})

    return json.dumps({"login": "success"})

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
