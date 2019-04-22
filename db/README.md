This is an sqlite3 database file which contains data such as the scoreboard,
task names, topic names, etc.

In order to check the content of the database file, you need sqlite3 installed.
```
> sqlite3
> .open cli_tasks.db
```

To see the tables and their schemas, simply run:
```
> .tables
> PRAGMA table_info(table_name);
```

# Tables
## Users

The users table.

Entry:
`id`         - int, unique id for each user
`username`   - text, the username of the user
`first_name` - text, first name of the user
`last_name`  - text, last name of the user

# Topics

Contains list of topics.

Entry:
`id`   - int, unique id for each topic
`name` - text, topic name

# Checker languages

Supported checker languages. Strongly depends on the image it is run on.

Entry:
`id`   - int, language id
`name` - text, the name of the language. Example: bash, cpp, etc.

## Tasks

Contains info about each task.

Entry:
`id`                  - int, unique id for each task
`name`                - text, name of the task
`added_by`            - text, optional, a name or any string to represent who added it
`checker_name`        - text. The name of the checker file, including extension
`checker_language_id` - int. Taken from the checker languages table.
`description`         - text. The description of the task. Shown when the task
                      - is started.

# Topic tasks

One to many table which maps the tasks to the topic they should be in.

Entry:
`topic_id` - int, the topic id that the task belongs to
`task_id`  - int, the task id

## Scores

Contains score for each task for each user.

Entry:
`user_id` - int, the id of the user which finished the task
`task_id` - int, the task id
`score`   - real, the best score for the user for this task
