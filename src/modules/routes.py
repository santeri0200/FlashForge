# pylint: disable=no-else-return, redefined-builtin, inconsistent-return-statements, too-many-return-statements, too-many-branches, possibly-used-before-assignment
from config import app, test_env
from flask import render_template, request, redirect, url_for
from modules import database
from entities.reference import Article, Book, Inproceedings, Manual

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_reference/<ref_type>", methods=["GET", "POST"])
def add_ref(ref_type):
    match ref_type:
        case "article":
            if request.method == "GET":
                return render_template("create_reference_article.html")

            ref = Article(**(request.form))
            if not ref.validate():
                return render_template("create_reference_article.html",
                                       error=True, error_message="Invalid details")
            elif not database.add_reference(ref):
                return render_template("create_reference_article.html",
                                       error=True, error_message="Invalid details")
        case "book":
            if request.method == "GET":
                return render_template("create_reference_book.html")

            ref = Book(**(request.form))
            if not ref.validate():
                return render_template("create_reference_book.html",
                                       error=True, error_message="Invalid details")
            elif not database.add_reference(ref):
                return render_template("create_reference_book.html",
                                       error=True, error_message="Invalid details")
        case "inproceedings":
            if request.method == "GET":
                return render_template("create_reference_inproceedings.html")

            ref = Inproceedings(**(request.form))
            if not ref.validate():
                return render_template("create_reference_inproceedings.html",
                                       error=True, error_message="Invalid details")
            elif not database.add_reference(ref):
                return render_template("create_reference_inproceedings.html",
                                       error=True, error_message="Invalid details")
        case "manual":
            if request.method == "GET":
                return render_template("create_reference_manual.html")

            ref = Manual(**(request.form))
            if not ref.validate():
                return render_template("create_reference_manual.html",
                                       error=True, error_message="Invalid details")
            elif not database.add_reference(ref):
                return render_template("create_reference_manual.html",
                                       error=True, error_message="Invalid details")

        case _:
            return render_template("error.html", error="Invalid reference type!")

    return redirect(url_for("index"))

@app.route("/refs")
def refs_page():
    articles = [ref.details() for ref in database.get_all_articles()]
    books    = [ref.details() for ref in database.get_all_books()]
    inproceedings = [ref.details() for ref in database.get_all_inproceedings()]

    refs = articles + books + inproceedings
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
    articles, books, inproceedings, manuals = database.search_result(query)
    books = [Book(**params._asdict()).details() for params in books]
    articles = [Article(**params._asdict()).details() for params in articles]
    inproceedings = [Inproceedings(**params._asdict()).details() for params in inproceedings]
    manuals = [Manual(**params._asdict()).details() for params in manuals]
    return render_template("refs.html", references=books+articles+inproceedings, title="Search results")

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
        ref = Article(**database.ref_from_id(ref_type, id)._asdict()).details()
    elif ref_type == "book":
        ref = Book(**database.ref_from_id(ref_type, id)._asdict()).details()
    elif ref_type == "inproceedings":
        ref = Inproceedings(**database.ref_from_id(ref_type, id)._asdict()).details()
    elif ref_type == "manual":
        ref = Manual(**database.ref_from_id(ref_type, id)._asdict()).details()

    if request.method == "GET":
        if ref:
            return render_template("edit_ref.html", ref=ref)
        else:
            return "Reference not found", 404
    if request.method == "POST":
        try:
            if ref_type == "article":
                edited_ref = Article(**(request.form), id=int(id))
                if not edited_ref.validate():
                    return render_template("edit_ref.html", ref=ref, error=True, error_message="Invalid details")
                if not database.edit_ref(ref_type, id, edited_ref.details()):
                    return render_template("edit_ref.html", ref=ref, error=True, error_message="Invalid details")
                return redirect(f"/{ref_type}/{id}")

            elif ref_type == "book":
                edited_ref = Book(**(request.form), id=int(id))
                if not edited_ref.validate():
                    return render_template("edit_ref.html", ref=ref, error=True, error_message="Invalid details")
                if not database.edit_ref(ref_type, id, edited_ref.details()):
                    return render_template("edit_ref.html", ref=ref, error=True, error_message="Invalid details")
                return redirect(f"/{ref_type}/{id}")

            elif ref_type == "inproceedings":
                edited_ref = Inproceedings(**(request.form), id=int(id))
                if not edited_ref.validate():
                    return render_template("edit_ref.html", ref=ref, error=True, error_message="Invalid details")
                if not database.edit_ref(ref_type, id, edited_ref.details()):
                    return render_template("edit_ref.html", ref=ref, error=True, error_message="Invalid details")
                return redirect(f"/{ref_type}/{id}")

            elif ref_type == "manual":
                edited_ref = Manual(**(request.form), id=int(id))
                if not edited_ref.validate():
                    return render_template("edit_ref.html", ref=ref, error=True, error_message="Invalid details")
                if not database.edit_ref(ref_type, id, edited_ref.details()):
                    return render_template("edit_ref.html", ref=ref, error=True, error_message="Invalid details")
                return redirect(f"/{ref_type}/{id}")

        except ValueError:
            return render_template("edit_ref.html", ref=ref, error=True, error_message="Invalid details")

@app.route("/delete/<ref_type>/<id>", methods=["GET", "POST"])
def reference_delete(ref_type, id):
    if ref_type == "article":
        article = Article(**database.ref_from_id(ref_type, id)._asdict()).details()
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
    elif ref_type == "book":
        book = Book(**database.ref_from_id(ref_type, id)._asdict()).details()
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
    elif ref_type == "inproceedings":
        inproceedings = Inproceedings(**database.ref_from_id(ref_type, id)._asdict()).details()
        if request.method == "GET":
            if inproceedings:
                return render_template("delete_ref.html", ref=inproceedings)
            else:
                return "Inproceedings reference not found", 404
        if request.method == "POST":
            if database.delete_reference(ref_type, id):
                return redirect("/")
            else:
                return render_template("error.html", error="Something went wrong.")
    elif ref_type == "manual":
        inproceedings = Manual(**database.ref_from_id(ref_type, id)._asdict()).details()
        if request.method == "GET":
            if manual:
                return render_template("delete_ref.html", ref=inproceedings)
            else:
                return "Inproceedings reference not found", 404
        if request.method == "POST":
            if database.delete_reference(ref_type, id):
                return redirect("/")
            else:
                return render_template("error.html", error="Something went wrong.")
