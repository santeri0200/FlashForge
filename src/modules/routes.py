# pylint: disable=no-else-return, redefined-builtin, inconsistent-return-statements
from config import app, test_env
from flask import render_template, request, redirect, url_for, Response
from modules import database

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_reference/article", methods=["GET", "POST"])
def add_ref():
    # pylint: disable=possibly-used-before-assignment
    if request.method == "GET":
        return render_template("create_reference_article.html")
    if request.method == "POST":
        failed = False
        try:
            author = request.form.get("author")
            title = request.form.get("title")
            journal = request.form.get("journal")
            year = int(request.form.get("year"))

        except ValueError:
            return render_template("create_reference_article.html", error=True, error_message="Invalid details")

        try:
            volume = request.form.get("volume") or None
            volume = int(volume) if volume else volume
            number = request.form.get("number") or None
            number = int(number) if number else number
            pages = request.form.get("pages") or None
            month = request.form.get("month") or None
            note = request.form.get("note") or None

        except ValueError:
            return render_template(
                "create_reference_article.html",
                error=True,
                error_message="Invalid optional details"
            )

        if len(author) > 100:
            failed = True
            message = "Name of author cannot exceed 100 characters"

        if len(title) > 500:
            failed = True
            message = "Title cannot exceed 500 characters"

        if len(journal) > 100:
            failed = True
            message = "Name of journal cannot exceed 100 characters"

        if year < 1900 or year > 2099:
            failed = True
            message = "Year must be set between 1900 and 2099"



        if failed:
            return render_template("create_reference_article.html", error=True, error_message=message)

        if database.add_article(author, title, journal, year, volume, number, pages, month, note):
            return redirect(url_for("index"))
        else:
            return render_template("create_reference_article.html", error=True, error_message="Invalid details")

@app.route("/refs")
def refs_page():
    refs=database.get_all_articles()
    return render_template("refs.html", references=refs)

if test_env:
    print("should be here!!!")
    @app.route("/reset_db")
    def reset_database():
        database.reset_db()
        return "db reset", 200

@app.route("/result")
def search_results():
    query = request.args.get('query')
    result = database.search_result(query)
    return render_template("refs.html", references=result, title="Search results")

@app.route("/article/<id>")
def article_page(id):
    article = database.article_from_id(id)
    if article:
        return render_template("article.html", article=article)
    else:
        return "Article not found", 404

@app.route("/edit/article/<id>", methods=["GET", "POST"])
def article_edit(id):
    # pylint: disable=possibly-used-before-assignment
    # pylint: disable=too-many-return-statements, too-many-branches
    article = database.article_from_id(id)
    if request.method == "GET":
        if article:
            return render_template("edit_article.html", article=article)
        else:
            return "Article not found", 404
    if request.method == "POST":
        failed = False
        try:
            author = request.form.get("author")
            title = request.form.get("title")
            journal = request.form.get("journal")
            year = int(request.form.get("year"))

        except ValueError:
            return render_template("edit_article.html", error=True, error_message="Invalid details")

        try:
            volume = request.form.get("volume") or None
            volume = int(volume) if volume else volume
            number = request.form.get("number") or None
            number = int(number) if number else number
            pages = request.form.get("pages") or None
            month = request.form.get("month") or None
            note = request.form.get("note") or None

        except ValueError:
            return render_template(
                "create_reference_article.html",
                error=True,
                error_message="Invalid optional details"
            )

        if len(author) > 100:
            failed = True
            message = "Name of author cannot exceed 100 characters"

        if len(title) > 500:
            failed = True
            message = "Title cannot exceed 500 characters"

        if len(journal) > 100:
            failed = True
            message = "Name of journal cannot exceed 100 characters"

        if year < 1900 or year > 2099:
            failed = True
            message = "Year must be set between 1900 and 2099"

        if failed:
            return render_template("edit_article.html", article=article, error=True, error_message=message)

        if database.edit_article(id, author, title, journal, year, volume, number, pages, month, note):
            return redirect(f"/article/{id}")
        else:
            return render_template("edit_article.html",article=article, error=True, error_message="Invalid details")

@app.route("/delete/article/<id>", methods=["GET", "POST"])
def article_delete(id):
    article = database.article_from_id(id)
    if request.method == "GET":
        if article:
            return render_template("delete_article.html", article=article)
        else:
            return "Article not found", 404
    if request.method == "POST":
        if database.delete_article(id):
            return redirect("/")
        else:
            return render_template("error.html", error="Something went wrong.")

@app.route("/generate_bib")
def generate_bib():
    refs = database.get_all_articles()
    if refs:
        entry = ""
        for ref in refs:
            entry += f"""@article{{article-{ref.id},\
            \n\tauthor = {{{ref.author}}},\
            \n\ttitle = {{{ref.title}}},\
            \n\tjournal = {{{ref.journal}}},\
            \n\tyear = {{{ref.year}}}\
            \n}}\n\n"""

        response = Response(
            entry,
            mimetype="application/x-bibtex",
            content_type="application/x-bibtex; charset=utf-8",
            headers={"Content-Disposition": "attachment;filename=references.bib"}
        )
        return response
    else:
        return render_template("error.html", error="No references found.")
