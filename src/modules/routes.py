from config import app, db, test_env
from flask import render_template, request, redirect, url_for
from modules import database
from sqlalchemy import text

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_reference/article", methods=["GET", "POST"])
def add_ref():
    if request.method == "GET":
        return render_template("create_reference_article.html")
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
        
@app.route("/refs")
def refs():
    refs=database.get_all_articles()
    return render_template("refs.html", references=refs)

if test_env:
    print("should be here!!!")
    @app.route("/reset_db")
    def reset_database():
        database.reset_db()
        return "db reset", 200
