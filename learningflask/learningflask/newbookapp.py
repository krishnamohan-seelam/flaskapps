import collections
import json
import jwt
import datetime
from flask import Flask, jsonify, request, Response
from werkzeug.exceptions import HTTPException, NotFound, BadRequest
from settings import *
from bookmodel import *
from usermodel import User
from functools import wraps
BOOK_KEYS = ('title', 'price', 'isbn')

def token_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        token = request.args.get('token')
        return f(*args,**kwargs)
        try:
            jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'error':'Need valid token to view this page'})   
    return wrapper

def validate(book, validate_keys=BOOK_KEYS):
    if (isinstance(validate_keys, collections.Sequence)) & (not isinstance(validate_keys, set)):
        validate_keys = set(validate_keys)
    return(validate_keys.issubset(book.keys()))


@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])
    if User.user_password_match(username, password):
        expiration_date = datetime.datetime.now() + datetime.timedelta(seconds=600)
        token  = jwt.encode({'exp':expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        response = Response("", 401, mimetype="application/json")
        return  response


@app.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})

@app.route('/books/<int:isbn>')
def getbook(isbn):
    book = Book.get_book(isbn)
    return jsonify(book)

@app.route('/books', methods=['POST'])
@token_required
def add_book():
    request_body = request.get_json()
    if validate(request_body):
        Book.add_book(request_body['title'],request_body['price'],request_body['isbn'])
        response = Response("", 201, mimetype="application/json")
        response.headers['Location'] = "/books/"+str(request_body['isbn'])
        return response
    else:
        invalidBookErrorMessage = {
            'errorMessage': 'Invalid book object passed in request',
            'helpString': "Data should be in {'title':'bookname','price':0.00,'isbn':0}"
        }
        response = Response(json.dumps(invalidBookErrorMessage),
                            400, mimetype="application/json")
        return response

@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
def update_book_by_isbn(isbn):
    request_body = request.get_json()
    if not validate(request_body,['title','price']):
        invalidBookErrorMessage = {
            'errorMessage': 'Invalid book object passed in request',
            'helpString': "Data should be in {'title':'bookname','price':0.00}"
        }
        response = Response(json.dumps(invalidBookErrorMessage),
                            400, mimetype="application/json")
        return response
    Book.replace_book(isbn,request_body['title'],request_body['price'])
    response = Response("", 204)
    response.headers['Location'] = "/books/"+str(isbn)
    return response

@app.route('/books/<int:isbn>', methods=['PATCH'])
@token_required
def update_book_fields_by_isbn(isbn):
    request_body = request.get_json()
    if ("title" in request_body):
        Book.update_book_title(isbn,request_body['title'])
    if ("price" in request_body):
        Book.update_book_price(isbn,request_body['price'])
    response = Response("", 204)
    response.headers['Location'] = "/books/"+str(isbn)
    return response

@app.route('/books/<int:isbn>', methods=['DELETE'])
@token_required
def delete_by_isbn(isbn):
    if(Book.delete_book(isbn)):
        response = Response("", 204)
        response.headers['Location'] = "/books/"+str(isbn)
        return response

    invalidBookErrorMessage = {
            'errorMessage': 'Book with ISBN not found',
        }
    response = Response(json.dumps(invalidBookErrorMessage),
                        400, mimetype="application/json")
    return response

if __name__ == '__main__':
    app.run(port=2121, debug=True)