echo "Creating database..."
createdb ohtu || exit 1

echo "Adding schema"
psql -d ohtu < schema.sql

echo "Installing dependencies"
poetry install || exit 1

echo "Running flask server"
flask --app src/app run --debug
