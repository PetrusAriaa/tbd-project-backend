from crypt import methods
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from psycopg2 import OperationalError

from lib.author import Author
from lib.book import Book
from lib.employee import Employee
from lib.store import Store
from lib.transaction import Transaction

app = Flask(__name__)
CORS(app)

@app.route('/<int:store_id>/books', methods=['GET', 'POST'])
def books(store_id):
    
    if request.method == 'GET':
        try:
            data, msg = Book.get_books(store_id)
            res = jsonify({
                "items": data,
                "length": len(data),
                "message": msg
            })
            if msg == "success":
                return make_response(res, 200)
            elif msg == "Not Found!":
                return make_response(res, 404)
            else:
                return make_response(res, 500)
        except Exception as err:
            return err
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            req = {
                "store": data.get('store'),
                "book_name": data.get('book_name'),
                "publication_year": data.get('publication_year'),
                "pages": data.get('pages'),
                "pname": data.get('pname'),
                "quantity": data.get('quantity'),
                "price": data.get('price'),
            }
            msg = Book.add_book(req)
            res = jsonify({"item": req, "message": msg})
            if msg == "success":
                return make_response(res, 200)
            else:
                return make_response(res, 400)
        except Exception as err:
            return err


@app.route('/<int:store_id>/books/<int:book_id>', methods=['GET', 'UPDATE', 'DELETE'])
def book(store_id, book_id):
    
    if request.method == 'GET':
        try:
            data, msg = Book.get_book(store_id, book_id)
            res = jsonify({
                "items": data,
                "length": len(data),
                "message": msg
            })
            if msg == "success":
                return make_response(res, 200)
            elif msg == "Not Found!":
                return make_response(res, 404)
            else:
                return make_response(res, 500)
        except Exception as err:
            return err


@app.route('/authors', methods=['GET'])
def authors():
    
    if request.method == 'GET':
        try:
            data = Author.get_authors()
            res = jsonify(data)
            return res
        except Exception as err:
            return err


@app.route('/employees', methods=['GET'])
def employees():
    
    if request.method == 'GET':
        try:
            data = Employee.get_employees()
            res = jsonify(data)
            return res
        except Exception as err:
            return err


@app.route('/stores/', methods=['GET'])
def stores():
    
    if request.method == 'GET':
        try:
            data = Store.get_stores()
            res = jsonify(data)
            return res
        except Exception as err:
            return err


@app.route('/<int:store_id>/transactions', methods=['GET'])
def transaction(store_id):
    
    if request.method == 'GET':
        try:
            data = Transaction.get_transaction(store_id)
            res = jsonify(data)
            return res
        except Exception as err:
            return err



if __name__ == '__main__':
    app.run()