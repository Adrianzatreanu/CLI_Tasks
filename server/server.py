from flask import Flask, request
from flask_cors import CORS
from shutil import copyfile
import json
import os
import subprocess
from time import sleep

from sanitychecker import SanityChecker
from dbhandler import DbHandler
from state import State
from filedownloader import FileDownloader

PATH_TO_SERVER="server/"
app = Flask(__name__)
CORS(app)
states = dict()

SSH_SHARED_COMM_CONFIG = """
host *
    controlmaster auto
    controlpath /tmp/ssh-%r@%h:%p
"""

ENV_VARS_LOCATION = "/.env_vars"

def check_login(username):
    # currently only checks for the username.
    # should actually use an authentication service
    return DbHandler.username_exists(username)

def create_folder_structure(username):
    containers_dir_path = PATH_TO_SERVER + "containers"
    if not os.path.exists(containers_dir_path):
        os.mkdir(containers_dir_path)
    user_dir_path = PATH_TO_SERVER + "containers/" + username
    if not os.path.exists(user_dir_path):
        os.mkdir(user_dir_path)
    vagrant_file_path = user_dir_path + "/Vagrantfile"
    if not os.path.exists(vagrant_file_path):
        copyfile(PATH_TO_SERVER + "Vagrantfile", vagrant_file_path)

def destroy_container(env, username):
    try:
        p = subprocess.Popen(["vagrant", "--vm-name=" + username, "destroy"], env=env, stdout=subprocess.PIPE)
        p.wait()
        print("Destroyed")
    except Exception as e:
        print("Machine did not exist so it could not be destroyed")
        print(str(e))
    return True

def create_container(env, username):
    p = subprocess.Popen(["vagrant", "--vm-name=" + username, "up"], env=env, stdout=subprocess.PIPE)
    print(p.communicate()[0].decode('utf-8'))
    p.wait()
    print("Machine brought up.")
    return True

def create_ssh_config(env, username, ssh_config_file_path):
    with open(ssh_config_file_path, 'w') as output:
        p = subprocess.Popen(["vagrant", "--vm-name=" + username, "ssh-config"], env=env, stdout=output)
        p.wait()
        print("Config file written")
    return True

def create_scripts_dir(env, username, ssh_config_file_path):
    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "mkdir", "/scripts"]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "chmod", "777", "/scripts"]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()
    return True

def create_chroot(env, username, ssh_config_file_path):
    TARGETDIR = "/mnt/chroot"
    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "mkdir", TARGETDIR]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "mkdir", TARGETDIR + "/proc"]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "mkdir", TARGETDIR + "/sys"]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "mkdir", TARGETDIR + "/dev"]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "mkdir", TARGETDIR + "/dev/shm"]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "mkdir", TARGETDIR + "/dev/pts"]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "mkdir", TARGETDIR + "/bin"]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "mkdir", TARGETDIR + "/lib"]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "mount", "--bind", "/proc/", TARGETDIR + "/proc"]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "mount", "-t", "sysfs", "sysfs", TARGETDIR + "/sys"]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "mount", "-t", "devtmpfs", "devtmpfs", TARGETDIR + "/dev"]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "mount", "-t", "tmpfs", "tmpfs", TARGETDIR + "/dev/shm"]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "mount", "-t", "devpts", "devpts", TARGETDIR + "/dev/pts"]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "ln", "/bin", TARGETDIR + "/bin"]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "mount", "--bind", "/lib", TARGETDIR + "/lib"]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    return True

def init_state(env, username, ssh_config_file_path):
    global states
    states[username] = State(username)
    states[username].set_cwd("~")

    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "touch", ENV_VARS_LOCATION]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "chmod", "777", ENV_VARS_LOCATION]
    p = subprocess.Popen(split_cmd, env=env, stdout=subprocess.PIPE)
    print(p.communicate())
    p.wait()

    return True

def init_resources(username):
    create_folder_structure(username)

    user_dir_path = PATH_TO_SERVER + "containers/" + username
    ssh_config_file_path = user_dir_path + "/ssh_config"

    new_env = os.environ
    new_env["VAGRANT_CWD"] = user_dir_path

    if not destroy_container(new_env, username):
        return False

    if not create_container(new_env, username):
        return False

    if not create_ssh_config(new_env, username, ssh_config_file_path):
        return False

    if not create_scripts_dir(new_env, username, ssh_config_file_path):
        return False

    if not init_state(new_env, username, ssh_config_file_path):
        return False


    # TODO: fix this
    # if not create_chroot(new_env, username, ssh_config_file_path):
    #     return False

    return True

def task_completed(username, task):
    if task == "test_task":
        return True

    user_dir_path = PATH_TO_SERVER + "containers/" + username
    new_env = os.environ
    new_env["VAGRANT_CWD"] = user_dir_path

    ssh_config_file_path = user_dir_path + "/ssh_config"
    script_location = DbHandler.get_checker_name(task)
    script_location = "/scripts/" + script_location

    checker_language = DbHandler.get_checker_language(task)
    print(checker_language)

    if checker_language == "shell":
        split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "chmod", "777", script_location]
        p = subprocess.Popen(split_cmd, env=new_env, stdout=subprocess.PIPE)
        p.wait()
        split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", script_location]
        p = subprocess.Popen(split_cmd, env=new_env, stdout=subprocess.PIPE)
        p.wait()
        print(p.returncode)
        return p.returncode == 0
    return False

def calculate_score(seconds):
    # eventually should use some custom formula for each task
    return 100

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

@app.route('/initialize_resources', methods=['POST'])
def initialize_resources():
    if request.method != "POST":
        return json.dumps({"initialize_resources": "Only POST is supported"})
    data = request.get_json(force=True)

    sanity_check_result = SanityChecker.perform_login_sanity_checks(data)
    if sanity_check_result != SanityChecker.OK:
        return json.dumps({"initialize_resources": sanity_check_result})

    username = data["username"]

    if not init_resources(username):
        return json.dumps({"initialize_resources": "failed"})

    return json.dumps({"initialize_resources": "success"})

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

@app.route('/initialize_task', methods=['POST'])
def initialize_task():
    if request.method != "POST":
        return json.dumps({"initialize_task": "Only POST is supported"})

    data = request.get_json(force=True)

    sanity_check_result = SanityChecker.perform_initialize_task_desc_sanity_checks(data)
    if sanity_check_result != SanityChecker.OK:
        return json.dumps({"initialize_task": sanity_check_result})

    task = data["task"]
    username = data["username"]

    user_dir_path = PATH_TO_SERVER + "containers/" + username
    new_env = os.environ
    new_env["VAGRANT_CWD"] = user_dir_path

    topic = DbHandler.get_topic_of_task(task)
    script_name = DbHandler.get_checker_name(task)

    if script_name == "":
        json.dumps({"initialize_task": "Could not find task"})

    # download
    script_github_path = "scripts/" + topic.lower() + "/" + script_name
    script_download_destination = PATH_TO_SERVER + "containers/" + username + "/" + script_name
    FileDownloader.download_file(username, script_github_path, script_download_destination)

    # upload
    p = subprocess.Popen(["vagrant", "--vm-name=" + username, "upload", script_download_destination, "/scripts/" + script_name], env=new_env, stdout=subprocess.PIPE)
    p.wait()

    # clean
    p = subprocess.Popen(["rm", script_download_destination], env=new_env, stdout=subprocess.PIPE)

    return json.dumps({"initialize_task": "done"})

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

def change_directory(cmd, username):
    global states
    print("here" + states[username].get_cwd())
    cmd.append("cd")
    cmd.append(states[username].get_cwd())
    cmd.append(";")

def save_env_vars(cmd):
    cmd.append("; echo")
    cmd.append("$PWD")
    cmd.append(">")
    cmd.append(ENV_VARS_LOCATION)

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


    user_dir_path = PATH_TO_SERVER + "containers/" + username
    new_env = os.environ
    new_env["VAGRANT_CWD"] = user_dir_path

    ssh_config_file_path = user_dir_path + "/ssh_config"

    split_cmd = cmd.split(' ')
    initial_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C"]
    change_directory(initial_cmd, username)
    split_cmd = initial_cmd + split_cmd
    save_env_vars(split_cmd)
    print(split_cmd)
    p = subprocess.Popen(split_cmd, env=new_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    p.wait()

    output = output.decode('utf-8')
    err = err.decode('utf-8')
    if output == "":
        output = err

    p = subprocess.Popen(["ssh", "-F", ssh_config_file_path, username, "-C", "cat", ENV_VARS_LOCATION, "|", "tr", "'\n'", "' '"], env=new_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    env_var_output, err = p.communicate()
    p.wait()

    states[username].set_cwd(env_var_output.decode('utf-8'))
    print(env_var_output.decode('utf-8'))
    # TODO: fix
    # TARGETDIR = "/mnt/chroot"
    # split_cmd = ["ssh", "-F", ssh_config_file_path, username, "-C", "sudo", "chroot", TARGETDIR, "pwd"]
    # p = subprocess.Popen(split_cmd, env=new_env, stdout=subprocess.PIPE)
    # print(p.communicate())
    # p.wait()

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
        return json.dumps({"check_task": "failed", "message": message})

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
