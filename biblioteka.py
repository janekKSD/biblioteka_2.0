#biblioteka

from app import app, db
from app.models import Book, Author, Book_list
from app.forms import BookForm

from flask import Flask, request, render_template, redirect, url_for

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Book": Book,
        "Author": Author,
        "Book_list": Book_list
    }

@app.route('/list/', methods=["GET", "POST"])
def list():
    form = BookForm()
    books_list = Book_list.query.all()
    if request.method == "POST":
        if form.validate_on_submit():
            new_book_id = Book.add_book(form.data)
            new_author_id = Author.add_author(form.data)
            Book_list.add_positon(new_book_id, new_author_id)
        return redirect(url_for("list"))
   
    return render_template("list.html", books_list=books_list, Book=Book, Author=Author, form=form)

@app.route("/position/<int:position_id>/", methods=["GET", "POST"])
def position_details(position_id):
    data = Book_list.get_position(position_id)
    form = BookForm(data = data)

    if request.method == "POST":
        if form.validate_on_submit():
            Book_list.update_position(position_id, form.data)
        return redirect(url_for("list"))

    return render_template("position.html", form=form, position_id=position_id)

if __name__ == "__main__":
    app.run(debug=True)
