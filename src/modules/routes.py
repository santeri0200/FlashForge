from config import app
from flask import render_template, request, redirect, url_for
from modules import database


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_reference/article", methods=["GET", "POST"])
def add_ref():
    if request.method == "GET":
        return render_template("create_reference_article.html")
    if request.method == "POST":
        author = request.form.get("author")
        title = request.form.get("title")
        journal = request.form.get("journal")
        year = request.form.get("year")
        if database.add_article(author, title, journal, year):
            return redirect(url_for("index"))
