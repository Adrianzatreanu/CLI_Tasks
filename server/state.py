class State:
    def __init__(self, username):
        self.username = username
        self.env_vars = dict()

    def get_cwd(self):
        return self.env_vars["CWD"]

    def set_cwd(self, cwd):
        self.env_vars["CWD"] = cwd
