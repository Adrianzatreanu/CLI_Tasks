import sqlite3
import sys

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

    @staticmethod
    def get_all_tasks():
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()

            instruction = "select name from tasks"
            cursor.execute(instruction)
            rows = cursor.fetchall()

            tasks = []

            for row in rows:
                tasks.append(row[0])

            return tasks

    @staticmethod
    def get_task_desc(task):
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()

            instruction = "select description from tasks where name='{}'".format(task)
            cursor.execute(instruction)
            row = cursor.fetchone()

            if row is None:
                return "Could not find task " + str(task)

            return row[0]

    @staticmethod
    def get_score_for_user(username):
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()

            instruction = "select id from users where username='{}'".format(username)
            cursor.execute(instruction)
            row = cursor.fetchone()

            if row is None:
                return 0.0

            user_id = row[0]

            instruction = "select sum(score) from scores where user_id={}".format(user_id)
            cursor.execute(instruction)
            row = cursor.fetchone()

            if row is None:
                return 0.0

            return row[0]

    @staticmethod
    def get_score(username, task):
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()

            instruction = "select id from users where username='{}'".format(username)
            cursor.execute(instruction)
            row = cursor.fetchone()

            if row is None:
                return 0.0

            user_id = row[0]

            instruction = "select id from tasks where name='{}'".format(task)
            cursor.execute(instruction)
            row = cursor.fetchone()

            if row is None:
                return 0.0

            task_id = row[0]

            instruction = "select score from scores where user_id={} and task_id={}".format(user_id, task_id)
            cursor.execute(instruction)
            row = cursor.fetchone()

            if row is None:
                return 0.0

            return row[0]

    @staticmethod
    def update_score(username, task, new_score):
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()

            instruction = "select id from users where username='{}'".format(username)
            cursor.execute(instruction)
            row = cursor.fetchone()

            if row is None:
                return

            user_id = row[0]
            print(user_id)

            instruction = "select id from tasks where name='{}'".format(task)
            cursor.execute(instruction)
            row = cursor.fetchone()

            if row is None:
                return

            task_id = row[0]

            instruction = "select score from scores where user_id={} and task_id={}".format(user_id, task_id)
            cursor.execute(instruction)
            row = cursor.fetchone()

            if row is None:
                instruction = "insert into scores(user_id, task_id, score) values({}, {}, {})".format(user_id, task_id, new_score)
                cursor.execute(instruction)
                conn.commit()
                return

            instruction = "update scores set score={} where user_id={} and task_id={}".format(new_score, user_id, task_id)
            cursor.execute(instruction)
            conn.commit()

    @staticmethod
    def get_checker_name(task):
        with sqlite3.connect(PATH_TO_DB) as conn:
            cursor = conn.cursor()

            instruction = "select checker_name from tasks where name='{}'".format(task)
            cursor.execute(instruction)
            row = cursor.fetchone()

            if row is None:
                return ""

            return row[0]
