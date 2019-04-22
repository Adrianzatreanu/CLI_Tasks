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
