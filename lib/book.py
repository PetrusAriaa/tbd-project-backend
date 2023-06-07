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
                        SELECT b.book_number, b.book_name, au.author_name, b.publication_year, b.pages, b.pname, st.quantity, b.price FROM book b
                            JOIN stock st ON b.book_number=st.book_number
                            JOIN store s ON st.store_id=s.store_id
                            JOIN wrote w ON b.book_number=w.bnum
                            JOIN author au ON w.authnum=au.author_number
                        WHERE s.store_id={store_id} ORDER BY b.book_name ASC
                    """)
            data = c.fetchall()
            msg = "success"
            
            items = []
            for col in data:
                book = {
                    "book_number": col[0],
                    "book_name": col[1],
                    "author": col[2],
                    "publication_year": col[3],
                    "pages": col[4],
                    "publisher": col[5],
                    "quantity": col[6],
                    "price": col[7],
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
        
    def get_all_book():
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                    port=CREDENTIALS['PORT'],
                                    database=CREDENTIALS['DATABASE'],
                                    user=CREDENTIALS['USER'],
                                    password=CREDENTIALS['PASSWORD']
                                   )
            c = db.cursor() 
            c.execute(f"""
                        SELECT b.book_number, b.book_name, au.author_name, b.publication_year, b.pages, b.pname, b.price FROM book b
                            JOIN wrote w ON b.book_number=w.bnum
                            JOIN author au ON w.authnum=au.author_number
                        ORDER BY b.book_name ASC
                      """)
            data = c.fetchall()
            msg = "success"
            items = []
            for col in data:
                book = {
                    "book_number": col[0],
                    "book_name": col[1],
                    "author": col[2],
                    "publication_year": col[3],
                    "pages": col[4],
                    "publisher": col[5],
                    "price": col[6]
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
                        SELECT b.book_number, b.book_name, au.author_name, b.publication_year, b.pages, b.pname, st.quantity, b.price
                        FROM book b
	                        JOIN stock st ON b.book_number=st.book_number
	                        JOIN store s ON st.store_id=s.store_id
                            JOIN wrote w ON b.book_number=w.bnum
                            JOIN author au ON w.authnum=au.author_number
                        WHERE st.store_id={store_id} AND b.book_number={book_id}
                    """)
            data = c.fetchone()
            msg = "success"
            
            item = []
            if data != None:
                book = {
                        "book_number": data[0],
                        "book_name": data[1],
                        "author": data[2],
                        "publication_year": data[3],
                        "pages": data[4],
                        "publisher": data[5],
                        "quantity": data[6],
                        "price": data[7]
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
        author = str(req['penulis'])
        
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
                c.execute(f"""SELECT author_number FROM author WHERE author_name='{author}'""")
                auth_id = c.fetchone()
                author_number = auth_id[0]
                
                c.execute(f"""
                        BEGIN;
                        INSERT INTO book (book_number, book_name, publication_year, pages, pname, price)
                        VALUES({book_number}, '{book_name}', {publication_year}, {pages}, '{publisher}', {price});
                        
                        INSERT INTO stock (store_id, book_number, quantity)
                        VALUES({store}, {book_number}, {quantity});
                        
                        INSERT INTO wrote (bnum, authnum)
                        VALUES({book_number}, {author_number});
                        
                        COMMIT;
                        ROLLBACK
                        """)
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
    
    
    def delete_book(store_id, book_id):
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                    port=CREDENTIALS['PORT'],
                                    database=CREDENTIALS['DATABASE'],
                                    user=CREDENTIALS['USER'],
                                    password=CREDENTIALS['PASSWORD']
                                    )
            c = db.cursor()
            c.execute(f"""
                      BEGIN;
                      DELETE FROM stock
                      WHERE book_number={int(book_id)} AND store_id={int(store_id)};
                      
                      COMMIT;
                      ROLLBACK;
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
        
        author = req['author']
        book_name = req['book_name']
        pages = req['pages']
        publication_year = req['publication_year']
        publisher = req['publisher']
        price = req['price']
        
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                    port=CREDENTIALS['PORT'],
                                    database=CREDENTIALS['DATABASE'],
                                    user=CREDENTIALS['USER'],
                                    password=CREDENTIALS['PASSWORD']
                                    )
            c = db.cursor()
            c.execute(f"""
                      SELECT author_number FROM author
                      WHERE author_name='{author}';
                      """)
            _id = c.fetchone()
            auth_id = _id[0]
            
            c.execute(f"""
                      BEGIN;
                      UPDATE wrote
                      SET authnum={auth_id}
                      WHERE bnum={book_id};
                      
                      UPDATE book
                      SET book_name='{book_name}', publication_year={publication_year}, pages={pages}, pname='{publisher}', price={price}
                      WHERE book_number={book_id};
                      
                      COMMIT;
                      ROLLBACK;
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
        
    def delete_book_data(book_number):
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                    port=CREDENTIALS['PORT'],
                                    database=CREDENTIALS['DATABASE'],
                                    user=CREDENTIALS['USER'],
                                    password=CREDENTIALS['PASSWORD']
                                    )
            c = db.cursor()
            c.execute(f"""
                      BEGIN;
                      
                      DELETE FROM wrote
                      WHERE bnum={book_number};
                      
                      DELETE FROM stock
                      WHERE book_number={book_number};
                      
                      DELETE FROM bought
                      WHERE bnum={book_number};
                      
                      DELETE FROM book
                      WHERE book_number={book_number};
                      
                      COMMIT;
                      ROLLBACK;
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
    
    def get_book_by_id(book_number):
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                        port=CREDENTIALS['PORT'],
                                        database=CREDENTIALS['DATABASE'],
                                        user=CREDENTIALS['USER'],
                                        password=CREDENTIALS['PASSWORD']
                                        )
            c = db.cursor()
            c.execute(f"""
                        SELECT b.book_number, b.book_name, au.author_name, b.publication_year, b.pages, b.pname, b.price
                        FROM book b
                            JOIN wrote w ON b.book_number=w.bnum
                            JOIN author au ON w.authnum=au.author_number
                        WHERE b.book_number={book_number}
                    """)
            data = c.fetchone()
            msg = "success"
            
            item = []
            if data != None:
                book = {
                        "book_number": data[0],
                        "book_name": data[1],
                        "author": data[2],
                        "publication_year": data[3],
                        "pages": data[4],
                        "publisher": data[5],
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