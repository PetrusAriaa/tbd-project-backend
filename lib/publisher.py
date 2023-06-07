import psycopg2
from config import CREDENTIALS


class Publisher:
    
    
    def get_publishers():
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                port=CREDENTIALS['PORT'],
                                database=CREDENTIALS['DATABASE'],
                                user=CREDENTIALS['USER'],
                                password=CREDENTIALS['PASSWORD']
                                )
            c = db.cursor()
            c.execute('SELECT * FROM publisher')
            data = c.fetchall()
            msg = "success"
            
            items = []
            for col in data:
                author = {
                    "publisher_name": col[0],
                    "city": col[1],
                    "country": col[2],
                    "telephone": col[3],
                    "year_founded": col[3]
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