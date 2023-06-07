from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from lib.author import Author
from lib.book import Book
from lib.employee import Employee
from lib.store import Store
from lib.transaction import Transaction
from lib.publisher import Publisher
from lib.stock import Stock
from lib.sqlbuilder import SQLBuilder

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
                "penulis": data.get('penulis') #restart server please
            }
            msg = Book.add_book(req)
            res = jsonify({"item": req, "message": msg})
            if msg == "success":
                return make_response(res, 200)
            else:
                return make_response(res, 400)
        except Exception as err:
            return err


@app.route('/<int:store_id>/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
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
    
    if request.method == 'DELETE':
        try:
            msg = Book.delete_book(store_id, book_id)
            res = jsonify({"message":msg})
            if msg == "success":
                return make_response(res, 200)
            elif msg == "Not Found!":
                return make_response(res, 404)
            else:
                return make_response(res, 400)
        except Exception as err:
            return err
    
    if request.method == 'PUT':
        try:
            data = request.get_json()
            qty = data.get('quantity')
            msg = Stock.edit_stock(store_id, book_id, qty)
            res = {"message": msg}
            if msg == "success":
                return make_response(res, 200)
            else:
                return make_response(res, 400)
        except Exception as err:
            return err
            

@app.route('/authors', methods=['GET'])
def authors():
    
    if request.method == 'GET':
        try:
            data, msg = Author.get_authors()
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


@app.route('/publishers', methods=['GET'])
def publishers():
    if request.method == 'GET':
        try:
            data, msg = Publisher.get_publishers()
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

@app.route('/employees', methods=['GET'])
def employees():
    
    if request.method == 'GET':
        try:
            data = Employee.get_employees()
            res = jsonify(data)
            return res
        except Exception as err:
            return err


@app.route('/stores', methods=['GET'])
def stores():
    
    if request.method == 'GET':
        try:
            data, msg = Store.get_stores()
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


@app.route('/stores/<int:store_id>', methods=['GET'])
def store(store_id):
    if request.method == 'GET':
        try:
            data, msg = Store.get_store(store_id)
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

@app.route('/books', methods=['GET'])
def all_books():
    if request.method == 'GET':
        try:
            data, msg = Book.get_all_book()
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
            
@app.route('/books/<int:book_id>', methods=['GET', 'DELETE', 'PUT'])
def all_book(book_id):
    
    if request.method == 'GET':
        try:
            data, msg = Book.get_book_by_id(book_id)
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
    
    if request.method == 'PUT':
        try:
            data = request.get_json()
            req = {
                "author": data.get('author'), #restart server please
                "book_name": data.get('book_name'),
                "pages": data.get('pages'),
                "publication_year": data.get('publication_year'),
                "publisher": data.get('pname'),
                "price": data.get('price'),
            }
            msg = Book.edit_book(req, book_id)
            msg = "success"
            res = jsonify({"item": req, "message": msg})
            if msg == "success":
                return make_response(res, 200)
            else:
                return make_response(res, 400)
        except Exception as err:
            return err
    
    if request.method == 'DELETE':
        try:
            msg = Book.delete_book_data(book_id)
            res = jsonify({"message":msg})
            if msg == "success":
                return make_response(res, 200)
            elif msg == "Not Found!":
                return make_response(res, 404)
            else:
                return make_response(res, 400)
        except Exception as err:
            return err
    
@app.route('/sql', methods=['POST'])
def start_sql():
    if request.method == 'POST':
        try:
            req = request.get_json()
            print(req)
            data = SQLBuilder.start_query(req)
            return jsonify(data)
        except Exception as err:
            return err
        

if __name__ == '__main__':
    app.run()