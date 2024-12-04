# pylint: disable=no-else-return, redefined-builtin, inconsistent-return-statements
from config import app, test_env
from flask import render_template, request, redirect, url_for
from modules import database, validate
from entities.reference import Article, Book

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_reference/<ref_type>", methods=["GET", "POST"])
def add_ref(ref_type):
    # pylint: disable=possibly-used-before-assignment
    if ref_type == "article":
        if request.method == "GET":
            return render_template("create_reference_article.html")
        if request.method == "POST":
            try:
                author = request.form.get("author")
                title = request.form.get("title")
                journal = request.form.get("journal")
                year = int(request.form.get("year"))
            except ValueError:
                return render_template("create_reference_article.html", error=True, error_message="Invalid details")
            failed, message = validate.validate_ref("article", author, title, journal, year)
            if failed:
                return render_template("create_reference_article.html", error=True, error_message=message)
        
            if database.add_reference(ref_type, author, title, journal, year):
                return redirect(url_for("index"))
            else:
                return render_template("create_reference_article.html", error=True, error_message="Invalid details")
    
    if ref_type == "book":
        if request.method == "GET":
            return render_template("create_reference_book.html")
        if request.method == "POST":
            try:
                author = request.form.get("author")
                title = request.form.get("title")
                publisher = request.form.get("publisher")
                year = int(request.form.get("year"))
                address = request.form.get("address")
            except ValueError:
                return render_template("create_reference_book.html", error=True, error_message="Invalid details")
            failed, message = validate.validate_ref("book", author, year, title, publisher, address)
            if failed:
                return render_template("create_reference_article.html", error=True, error_message=message)
            if database.add_reference(ref_type, author, year, title, publisher, address):
                return redirect(url_for("index"))
            else:
                return render_template("create_reference_book.html", error=True, error_message="Invalid details")

@app.route("/refs")
def refs_page():
    refs = database.get_all_articles()
    
    articles = [Article(*params).details() for params in database.get_all_articles()]
    books = [Book(*params).details() for params in database.get_all_books()]

    refs = articles + books
    return render_template("refs.html", references=refs, articles=articles)

if test_env:
    print("should be here!!!")
    @app.route("/reset_db")
    def reset_database():
        database.reset_db()
        return "db reset", 200

@app.route("/result")
def search_results():
    query = request.args.get('query')
    articles, books = database.search_result(query)
    books = [Book(*params).details() for params in books]
    articles = [Article(*params).details() for params in articles]
    return render_template("search_results.html", references=books+articles)

@app.route("/<ref_type>/<id>")
def ref_page(ref_type, id):
    ref = database.ref_from_id(ref_type, id)
    if ref:
        return render_template(f"{ref_type}.html", ref=ref, ref_type=ref_type)
    else:
        return "Reference not found", 404
    
@app.route("/edit/<ref_type>/<id>", methods=["GET", "POST"])
def reference_edit(ref_type, id):
    if ref_type == "article":
        ref = Article(*database.ref_from_id(ref_type, id)).details()
    elif ref_type == "book":
        ref = Book(*database.ref_from_id(ref_type, id)).details()

    if request.method == "GET":
        if ref:
            return render_template("edit_ref.html", ref=ref)
        else:
            return "Reference not found", 404
    if request.method == "POST":
        try:
            if ref_type == "article":
                author = request.form.get("author")
                title = request.form.get("title")
                journal = request.form.get("journal")
                year = int(request.form.get("year"))
                details = {"author": author, "title": title, "journal": journal, "year": year}
            elif ref_type == "book":
                author = request.form.get("author")
                title = request.form.get("title")
                publisher = request.form.get("publisher")
                year = int(request.form.get("year"))
                address = request.form.get("address")
                details = {"author": author, "year": year, "title": title, "publisher": publisher, "address": address}
        except ValueError:
            return render_template("edit_ref.html", error=True, error_message="Invalid details")

        failed, message = validate.validate_ref(ref_type, *list(details.values()))
        if failed:
            return render_template("edit_ref", ref=ref, error=True, error_message=message)
        if database.edit_ref(ref_type, id, details):
            return redirect(f"/{ref_type}/{id}")
        else:
            return render_template("edit_ref.html", ref=ref, error=True, error_message="Invalid details")

@app.route("/delete/<ref_type>/<id>", methods=["GET", "POST"])
def reference_delete(ref_type, id):
    if ref_type == "article":
        article = Article(*database.ref_from_id(ref_type, id)).details()
        if request.method == "GET":
            if article:
                return render_template("delete_ref.html", ref=article)
            else:
                return "Article not found", 404
        if request.method == "POST":
            if database.delete_reference(ref_type, id):
                return redirect("/")
            else:
                return render_template("error.html", error="Something went wrong.")
    if ref_type == "book":
        book = Book(*database.ref_from_id(ref_type, id)).details()
        if request.method == "GET":
            if book:
                return render_template("delete_ref.html", ref=book)
            else:
                return "Book not found", 404
        if request.method == "POST":
            if database.delete_reference(ref_type, id):
                return redirect("/")
            else:
                return render_template("error.html", error="Something went wrong.")
