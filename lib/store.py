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
            msg = "success"
            
            items = []
            for col in data:
                store = {
                    "store_id": col[0],
                    "manager": col[1],
                    "street": col[2],
                    "city": col[3],
                    "state": col[4],
                    "country": col[5],
                }
                items.append(store)
            
            if len(items) == 0:
                msg = "Not Found!"
            
            c.close()
            db.close()
            return items, msg
        
        except (psycopg2.Error, psycopg2.DatabaseError) as err:
            c.close()
            db.close()
            return [], f'Error while connecting to PostgreSQL Database: {err}'
    
    
    def get_store(store_id):
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                port=CREDENTIALS['PORT'],
                                database=CREDENTIALS['DATABASE'],
                                user=CREDENTIALS['USER'],
                                password=CREDENTIALS['PASSWORD']
                                )
            c = db.cursor()
            c.execute(f"""SELECT * FROM store WHERE store_id={store_id}""")
            data = c.fetchone()
            msg = "success"
            
            item = []
            if data != None:
                store = {
                    "store_id": data[0],
                    "manager": data[1],
                    "street": data[2],
                    "city": data[3],
                    "state": data[4],
                    "country": data[5],
                }
                item.append(store)
            else:
                msg = "Not Found!"
            
            c.close()
            db.close()
            return item, msg
        
        except (psycopg2.Error, psycopg2.DatabaseError) as err:
            c.close()
            db.close()
            return [], f'Error while connecting to PostgreSQL Database: {err}'
    
    