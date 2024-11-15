# FlashForge
OHTU miniprojekti

[BACKLOG](https://github.com/users/santeri0200/projects/3)

## Running the project
1. Run your Postgresql service.
2. Create a database with `createdb`. The default used by the project is `ohtu`.
> You can combine these to `createdb ohtu`.
3. Add the database schema by running `psql -d ohtu < schema.sql`.
4. Install poetry dependencies with `poetry install`.
5. Open `poetry shell` and run the flask application with `flask --app src/app run --debug`.
