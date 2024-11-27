# FlashForge
OHTU miniprojekti

[BACKLOG](https://github.com/users/santeri0200/projects/3)
[USER STORIES](https://github.com/users/santeri0200/projects/4)

## Running the project
Run the project with `sh run_setup.sh`.
The script uses database `ohtu` which is the same as the default used without `.env`-file.

or

1. Run your Postgresql service.
2. Create a database with `createdb`. The default used by the project is `ohtu`.
> You can combine these to `createdb ohtu`.
3. Add the database schema by running `psql -d ohtu < schema.sql`.
4. Install poetry dependencies with `poetry install`.
5. Open `poetry shell` and run the flask application with `flask --app src/app run --debug`.

## Running tests

### Unittest

Run unittest with command: `poetry run pytest`

###Pylint

Run pylint with command: `pylint src`

###Robot tests

Run Robot tests with command: sh run_robot_tests.sh

## Definition of Done
- All subtasks marked on the task are done.
- CI is successful on the pull request.
- Pull request is approved by atleast one peer.
- Pull request merges to master without conflicts.

![Screenshot from 2024-11-20 14-22-15](https://github.com/user-attachments/assets/a0be1591-5cd4-4305-b378-586d864ef504)
