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

@app.route('/books', methods=['GET', 'POST'])
def books():
    
    if request.method == 'GET':
        try:
            data = Book.get_books()
            res = jsonify(data)
            return res
        except Exception as err:
            return err
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            req = {
                "store": data.get('store'),
                "book_number": data.get('book_number'),
                "book_name": data.get('book_name'),
                "publication_year": data.get('publication_year'),
                "pages": data.get('pages'),
                "pname": data.get('pname'),
                "quantity": data.get('quantity'),
                "price": data.get('price'),
            }
            res = Book.add_book(req)
            if res == 0:
                return jsonify({"message": "Operation Success"})
            else:
                raise OperationalError
        except Exception as err:
            return err
        

@app.route('/books/<int:id>', methods=['GET'])
def book(id):
    
    if request.method == 'GET':
        try:
            data = Book.get_book(id)
            res = jsonify(data)
            return res
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