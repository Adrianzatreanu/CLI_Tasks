import sqlite3

# if called from root directory
PATH_TO_DB = "db/cli_tasks.db"

class DbHandler:

    @staticmethod
    def list_topics():
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()
            instruction = "select name from topics"
            cursor.execute(instruction)
            rows = cursor.fetchall()

            topics = []
            for row in rows:
                topics.append(row[0])

            return topics

    @staticmethod
    def username_exists(username):
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()
            instruction = "select id from users where username='{}'".format(username)
            cursor.execute(instruction)
            row = cursor.fetchone()

            return row is not None

    @staticmethod
    def get_tasks(topic):
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()
            instruction = "select id from topics where name='{}'".format(topic)
            cursor.execute(instruction)
            row = cursor.fetchone()

            if row is None:
                return [], []

            topic_id = row[0]
            instruction = "select task_id from topic_tasks where topic_id={}".format(topic_id)
            cursor.execute(instruction)
            rows = cursor.fetchall()
            task_ids = []
            for row in rows:
                task_ids.append(row[0])

            tasks = []
            for task_id in task_ids:
                instruction = "select name from tasks where id={}".format(task_id)
                cursor.execute(instruction)
                row = cursor.fetchone()
                if row is not None:
                    tasks.append(row[0])

            return tasks, task_ids

    @staticmethod
    def add_scores_for_tasks(tasks, task_ids, username):
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()

            instruction = "select id from users where username='{}'".format(username)
            cursor.execute(instruction)
            row = cursor.fetchone()

            if row is None:
                return

            user_id = row[0]

            for idx, task_id in enumerate(task_ids):
                instruction = "select score from scores where task_id={} and user_id={}".format(task_id, user_id)
                cursor.execute(instruction)
                row = cursor.fetchone()

                if row is not None:
                    tasks[idx] += " (best: {}p)".format(row[0])

    @staticmethod
    def get_tasks_and_scores(topic, username):
        tasks, task_ids = DbHandler.get_tasks(topic)
        DbHandler.add_scores_for_tasks(tasks, task_ids, username)
        return tasks
