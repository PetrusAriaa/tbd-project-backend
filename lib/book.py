import psycopg2

from config import CREDENTIALS


class Book:
    
    
    def get_books(store_id):
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                port=CREDENTIALS['PORT'],
                                database=CREDENTIALS['DATABASE'],
                                user=CREDENTIALS['USER'],
                                password=CREDENTIALS['PASSWORD']
                                )
            c = db.cursor()
            c.execute(f"""
                        SELECT b.book_number, b.book_name, b.publication_year, b.pages, b.pname, st.quantity, b.price
                        FROM book b
                            JOIN stock st ON b.book_number=st.book_number
                            JOIN store s ON st.store_id=s.store_id
                        WHERE s.store_id={store_id} ORDER BY b.book_name ASC
                    """)
            data = c.fetchall()
            msg = "success"
            
            items = []
            for col in data:
                book = {
                    "book_number": col[0],
                    "book_name": col[1],
                    "publication_year": col[2],
                    "pages": col[3],
                    "publisher": col[4],
                    "quantity": col[5],
                    "price": col[6],
                }
                items.append(book)
            
            if len(items) == 0:
                msg = "Not Found!"
            
            c.close()
            db.close()
            return items, msg
        
        except (psycopg2.Error, psycopg2.DatabaseError) as err:
            c.close()
            db.close()
            return [], f'Error while connecting to PostgreSQL Database: {err}'
        
        
    def get_book(store_id, book_id):
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                    port=CREDENTIALS['PORT'],
                                    database=CREDENTIALS['DATABASE'],
                                    user=CREDENTIALS['USER'],
                                    password=CREDENTIALS['PASSWORD']
                                    )
            c = db.cursor()
            c.execute(f"""
                        SELECT b.book_number, b.book_name, b.publication_year, b.pages, b.pname, st.quantity, b.price
                        FROM book b
	                        JOIN stock st ON b.book_number=st.book_number
	                        JOIN store s ON st.store_id=s.store_id
                        WHERE st.store_id={store_id} AND b.book_number={book_id}
                    """)
            data = c.fetchone()
            msg = "success"
            
            item = []
            if data != None:
                book = {
                        "book_number": data[0],
                        "book_name": data[1],
                        "publication_year": data[2],
                        "pages": data[3],
                        "publisher": data[4],
                        "quantity": data[5],
                        "price": data[6]
                    }
                item.append(book)
            else:
                msg = "Not Found!"
            
            c.close()
            db.close()
            return item, msg
        
        except (psycopg2.Error, psycopg2.DatabaseError) as err:
            c.close()
            db.close()
            return [], f'Error while connecting to PostgreSQL Database: {err}'
    
    
    def add_book(req):
        
        store = int(req['store'])
        book_name = str(req['book_name'])
        publication_year = int(req['publication_year'])
        pages = int(req['pages'])
        publisher = str(req['pname'])
        quantity = int(req['quantity'])
        price = int(req['price'])
        
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                    port=CREDENTIALS['PORT'],
                                    database=CREDENTIALS['DATABASE'],
                                    user=CREDENTIALS['USER'],
                                    password=CREDENTIALS['PASSWORD']
                                    )
            c = db.cursor()
            c.execute(f"""SELECT book_number, book_name FROM book""")
            books = c.fetchall()
            msg = "success"
            
            _book_numbers = []
            _book_names = []
            for book in books:
                _book_numbers.append(book[0])
                _book_names.append(book[1])
            
            if not (book_name in _book_names):
                book_number = max(_book_numbers)+1
                c.execute(f"""INSERT INTO book (book_number, book_name, publication_year, pages, pname, price)
                      VALUES({book_number}, '{book_name}', {publication_year},
                      {pages}, '{publisher}', {price})""")
                c.execute(f"""INSERT INTO stock (store_id, book_name, quantity)
                          VALUES({store}, {book_number}, {quantity})""")
            else:
                msg = "Book Exists"
            
            c.close()
            db.commit()
            db.close()
            return msg
        
        except (psycopg2.Error, psycopg2.DatabaseError) as err:
            c.close()
            db.close()
            return f'Error while connecting to PostgreSQL Database: {err}'
    
    
    def delete_book(book_id):
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                    port=CREDENTIALS['PORT'],
                                    database=CREDENTIALS['DATABASE'],
                                    user=CREDENTIALS['USER'],
                                    password=CREDENTIALS['PASSWORD']
                                    )
            c = db.cursor()
            c.execute(f"""
                      DELETE FROM stock WHERE book_id={book_id}
                      """)
            c.execute(f"""
                      DELETE FROM book WHERE book_id={book_id}
                      """)
            msg = "success"
            
            c.close()
            db.commit()
            db.close()
            return msg
            
        except (psycopg2.Error, psycopg2.DatabaseError) as err:
            c.close()
            db.close()
            return f'Error while connecting to PostgreSQL Database: {err}'
    
    
    def edit_book(req, book_id):
        
        book_name = str(req['book_name'])
        publication_year = int(req['publication_year'])
        pages = int(req['pages'])
        publisher = str(req['pname'])
        price = int(req['price'])
        
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                    port=CREDENTIALS['PORT'],
                                    database=CREDENTIALS['DATABASE'],
                                    user=CREDENTIALS['USER'],
                                    password=CREDENTIALS['PASSWORD']
                                    )
            c = db.cursor()
            c.execute(f"""
                      UPDATE book
                      SET book_name='{book_name}', publication_year={publication_year}, pages={pages}, pname='{publisher}', price={price}
                      WHERE book_number={book_id}
                      """)
            msg = "success"
            
            c.close()
            db.commit()
            db.close()
            return msg
        
        except (psycopg2.Error, psycopg2.DatabaseError) as err:
            c.close()
            db.close()
            return f'Error while connecting to PostgreSQL Database: {err}'