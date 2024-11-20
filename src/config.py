from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

test_env = getenv("TEST_ENV") == "true"
print(f"Test environment: {test_env}")

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY", "MYSECRET")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL", "postgresql:///ohtu")
db = SQLAlchemy(app)
