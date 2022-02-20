# app/models.py
from pickle import TRUE
from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    author_id = db.relationship("Book_list", backref="title_book", lazy="dynamic")
    available = db.Column(db.Boolean)

    def __str__(self):
        return f"{self.title}"

    def add_book(data):
        title = data['title']
        new_book = Book.query.filter_by(title=title).first()
        if new_book:
            return new_book.id
        else:    
            available = data['available']
            new_book = Book(title=title, available=available)
            db.session.add(new_book)
            db.session.commit()
            return new_book.id 

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), index=True, unique=True)
    title_id = db.relationship("Book_list", backref="name_author", lazy="dynamic")

    def __str__(self):
        return f"{self.name}"

    def add_author(data):
        author = data['author']
        new_author = Author.query.filter_by(name=author).first()
        if new_author:
            return new_author.id
        else:
            new_author = Author(name=author)
            db.session.add(new_author)
            db.session.commit()
            return new_author.id

class Book_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __str__(self):
        return f"<Book list {self.id} title id {self.book_id} author id {self.author_id}>"

    def add_positon(id_book, id_author):
        new_position = Book_list(book_id=id_book, author_id=id_author)
        db.session.add(new_position)
        db.session.commit()

    def get_position(position_id):
        position = Book_list.query.get(position_id)
        title=Book.query.get(position.book_id)
        author=Author.query.get(position.author_id)
        available=Book.query.get(position.book_id).available
        data = {'title':title, 'author':author, 'available':available}
        return data

    def update_position(position_id, data):
        position = Book_list.query.get(position_id)
        book = Book.query.get(position.book_id)
        author = Author.query.get(position.author_id)
        author.name = data['author']
        db.session.add(author)
        book.title = data['title']
        book.available = data['available']
        db.session.add(book)
        db.session.commit() 
        