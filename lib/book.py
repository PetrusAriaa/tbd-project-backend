import psycopg2

from config import CREDENTIALS


class Book:
    
    
    def get_books():
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                port=CREDENTIALS['PORT'],
                                database=CREDENTIALS['DATABASE'],
                                user=CREDENTIALS['USER'],
                                password=CREDENTIALS['PASSWORD']
                                )
            c = db.cursor()
            c.execute('SELECT * FROM book')
            data = c.fetchall()
            
            res = []
            for col in data:
                book = {
                    "store": col[0],
                    "book_number": col[1],
                    "book_name": col[2],
                    "publication_year": col[3],
                    "pages": col[4],
                    "pname": col[5],
                    "quantity": col[6],
                    "price": col[7],
                }
                res.append(book)
            
            c.close()
            db.close()
            
            return res
        
        except (psycopg2.Error, psycopg2.DatabaseError) as err:
            c.close()
            db.close()
            return f'Error while connecting to PostgreSQL Database: {err}'
        
        
    def get_book(id):
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                    port=CREDENTIALS['PORT'],
                                    database=CREDENTIALS['DATABASE'],
                                    user=CREDENTIALS['USER'],
                                    password=CREDENTIALS['PASSWORD']
                                    )
            c = db.cursor()
            c.execute(f"""SELECT * FROM book
                      WHERE book_number={id}""")
            data = c.fetchone()
            res = {
                    "store": data[0],
                    "book_number": data[1],
                    "book_name": data[2],
                    "publication_year": data[3],
                    "pages": data[4],
                    "pname": data[5],
                    "quantity": data[6],
                    "price": data[7],
                }
            
            c.close()
            db.close()
            
            return res
        
        except (psycopg2.Error, psycopg2.DatabaseError) as err:
            c.close()
            db.close()
            return f'Error while connecting to PostgreSQL Database: {err}'
    
    
    def add_book(req):
        
        store = int(req['store'])
        book_name = str(req['book_name'])
        publication_year = int(req['publication_year'])
        pages = int(req['pages'])
        pname = str(req['pname'])
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
            c.execute(f"""SELECT book_number FROM book""")
            data = c.fetchall()
            _id = []
            for i in data:
                _id.append(i[0])
            
            book_number = max(_id)+1
            c.execute(f"""INSERT INTO book (store, book_number, book_name, publication_year, pages, pname, quantity, price)
                      VALUES({store}, {book_number}, '{book_name}', {publication_year}, {pages}, '{pname}', {quantity}, {price})""")
            
            c.close()
            db.commit()
            db.close()
            
            return 0
        
        except (psycopg2.Error, psycopg2.DatabaseError) as err:
            c.close()
            db.close()
            return f'Error while connecting to PostgreSQL Database: {err}'