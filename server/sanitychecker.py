class SanityChecker:
    OK = 0

    @staticmethod
    def perform_login_sanity_checks(data):
        res = ""

        if "username" not in data:
            res += "username missing."

        if res == "":
            return SanityChecker.OK
        return res

    @staticmethod
    def perform_execute_sanity_checks(data):
        res = ""

        if "cmd" not in data:
            res += "cmd missing."

        if "username" not in data:
            res += "username missing."

        if res == "":
            return SanityChecker.OK
        return res

    @staticmethod
    def perform_list_tasks_sanity_checks(data):
        res = ""

        if "topic" not in data:
            res += "topic missing."
        if "username" not in data:
            res += "username missing."

        if res == "":
            return SanityChecker.OK
        return res
