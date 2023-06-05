import psycopg2

from config import CREDENTIALS


class Author:
    
    
    def get_authors():
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                port=CREDENTIALS['PORT'],
                                database=CREDENTIALS['DATABASE'],
                                user=CREDENTIALS['USER'],
                                password=CREDENTIALS['PASSWORD']
                                )
            c = db.cursor()
            c.execute('SELECT * FROM author')
            data = c.fetchall()
            msg = "success"
            
            items = []
            for col in data:
                author = {
                    "author_number": col[0],
                    "author_name": col[1],
                    "year_born": col[2],
                    "year_died": col[3]
                }
                items.append(author)
            
            if len(items) == 0:
                msg = "Not Found!"
            
            c.close()
            db.close()
            return items, msg
        
        except (psycopg2.Error, psycopg2.DatabaseError) as err:
            c.close()
            db.close()
            return [], f'Error while connecting to PostgreSQL Database: {err}'