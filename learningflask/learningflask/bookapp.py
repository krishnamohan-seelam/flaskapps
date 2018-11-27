from flask import Flask, jsonify, request, Response
from werkzeug.exceptions import HTTPException, NotFound, BadRequest
import collections
import json
books = [
    {'title': 'ABC Rhymes',
     'price': 100,
     'isbn': 1
     },
    {'title': 'Learn Alphabets',
     'price': 75,
     'isbn': 2
     }
]
BOOK_KEYS = ('title', 'price', 'isbn')
bookapp = Flask(__name__)


def validate(book, validate_keys=BOOK_KEYS):
    if (isinstance(validate_keys, collections.Sequence)) & (not isinstance(validate_keys, set)):
        validate_keys = set(validate_keys)
    return(validate_keys.issubset(book.keys()))

# GET


@bookapp.route('/books')
def get_books():
    return jsonify({'books': books})

# GET BY KEY


@bookapp.route('/books/<int:isbn>')
def getbook(isbn):
    for book in books:
        if book['isbn'] == isbn:
            return jsonify({'title': book['title'], 'price': book['price']})
    return "None", 404

# POST


@bookapp.route('/books', methods=['POST'])
def add_book():
    request_body = request.get_json()
    if validate(request_body):
        add_book = {key: request_body[key] for key in BOOK_KEYS}
        books.append(add_book)
        response = Response("", 201, mimetype="application/json")
        response.headers['Location'] = "/books/"+str(add_book['isbn'])
        return response
    else:
        invalidBookErrorMessage = {
            'errorMessage': 'Invalid book object passed in request',
            'helpString': "Data should be in {'title':'bookname','price':0.00,'isbn':0}"
        }
        response = Response(json.dumps(invalidBookErrorMessage),
                            400, mimetype="application/json")
        return response

# PUT


@bookapp.route('/books/<int:isbn>', methods=['PUT'])
def update_book_by_isbn(isbn):
    request_body = request.get_json()
    new_book = {'title': request_body['title'],
                'price': request_body['price'],
                'isbn': isbn
                }
    book_index = 0
    for book in books:
        current_isbn = book['isbn']
        if (current_isbn == isbn):
            books[book_index] = new_book
        book_index += 1
    response = Response("", 204)
    return response

# PATCH


@bookapp.route('/books/<int:isbn>', methods=['PATCH'])
def update_book_fields_by_isbn(isbn):
    request_body = request.get_json()
    updated_book = {}
    if ("title" in request_body):
        updated_book['title'] = request_body['title']

    if ("price" in request_body):
        updated_book['price'] = request_body['price']

    for book in books:
        if book["isbn"] == isbn:
            book.update(updated_book)
    response = Response("", 204)
    response.headers['Location'] = "/books/"+str(isbn)
    return response

# DELETE


@bookapp.route('/books/<int:isbn>', methods=['DELETE'])
def delete_by_isbn(isbn):
    book_index = 0
    for book in books:
        if book["isbn"] == isbn:
            books.pop(book_index)
            response = Response("", 204)
            return response
        book_index += 1
        invalidBookErrorMessage = {
            'errorMessage': 'Book with ISBN not found',
        }
    response = Response(json.dumps(invalidBookErrorMessage),
                        400, mimetype="application/json")
    return response


if __name__ == '__main__':
    bookapp.run(port=2121, debug=True)
