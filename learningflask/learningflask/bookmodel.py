import json
from flask import Flask
from settings import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    isbn = db.Column(db.Integer)

    def add_book(_title, _price, _isbn):
        new_Book = Book(title=_title, price=_price, isbn=_isbn)
        db.session.add(new_Book)
        db.session.commit()

    def get_all_books():
        return [Book.json(book) for book in Book.query.all()]

    def get_book(_isbn):
        return Book.json(Book.query.filter_by(isbn=_isbn).first())

    def delete_book(_isbn):
        is_successful = Book.query.filter_by(isbn=_isbn).delete()
        db.session.commit()
        return bool(is_successful)

    def update_book_price(_isbn, _price):
        book = Book.query.filter_by(isbn=_isbn).first()
        book.price = _price
        db.session.commit()

    def update_book_title(_isbn, _title):
        book = Book.query.filter_by(isbn=_isbn).first()
        book.title = _title
        db.session.commit()

    def replace_book(_isbn, _title, _price):
        book = Book.query.filter_by(isbn=_isbn).first()
        book.title = _title
        book.price = _price
        db.session.commit()

    def json(self):
        return {'title': self.title, 'price': self.price, 'isbn': self.isbn}

    def __repr__(self):
        book_object = {'title': self.title,
                       'price': self.price, 'isbn': self.isbn}
        return json.dumps(book_object)
