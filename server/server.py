from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/execute', methods=['POST'])
def execute():
    if request.method != "POST":
        return json.dumps({"execute": "Only POST is supported"})
    data = request.get_json(force=True)
    cmd = ' '.join(data["cmd"])
    username = data["username"]
    output = "Command is not supported."
    print("Cmd is: " + str(cmd))

    if cmd == "ls":
        output = "a.txt\nb.txt\n"

    return json.dumps({"execute": output})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
