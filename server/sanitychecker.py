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

    @staticmethod
    def perform_get_score_for_user_sanity_checks(data):
        res = ""

        if "username" not in data:
            res += "username missing."

        if res == "":
            return SanityChecker.OK
        return res

    @staticmethod
    def perform_get_task_desc_sanity_checks(data):
        res = ""

        if "task" not in data:
            res += "task missing."

        if res == "":
            return SanityChecker.OK
        return res
