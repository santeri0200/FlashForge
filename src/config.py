from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY", "MYSECRET")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL", "postgresql:///ohtu")
db = SQLAlchemy(app)
