import psycopg2

from config import CREDENTIALS


class Store:
    
    
    def get_stores():
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                port=CREDENTIALS['PORT'],
                                database=CREDENTIALS['DATABASE'],
                                user=CREDENTIALS['USER'],
                                password=CREDENTIALS['PASSWORD']
                                )
            c = db.cursor()
            c.execute('SELECT * FROM store')
            data = c.fetchall()
            
            res = []
            for col in data:
                store = {
                    "store_id": col[0],
                    "manager": col[1],
                    "street": col[2],
                    "city": col[3],
                    "state": col[4],
                    "country": col[5],
                }
                res.append(store)
            
            c.close()
            db.close()
            
            return res
        
        except (psycopg2.Error, psycopg2.DatabaseError) as err:
            c.close()
            db.close()
            return f'Error while connecting to PostgreSQL Database: {err}'
    
    