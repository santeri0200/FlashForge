from config import app
from flask import render_template, request, redirect, url_for
from modules import database


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_reference/article", methods=["GET", "POST"])
def add_ref():
    if request.method == "GET":
        return render_template("create_reference_article.html", error=False)
    if request.method == "POST":
        try:
            author = request.form.get("author")
            title = request.form.get("title")
            journal = request.form.get("journal")
            year = int(request.form.get("year"))

        except ValueError:
            return render_template("create_reference_article.html", error=True, error_message="Virheelliset tiedot")

        if database.add_article(author, title, journal, year):
            return redirect(url_for("index"))
        else:
            return render_template("create_reference_article.html", error=True, error_message="Virheelliset tiedot")

