import psycopg2

from config import CREDENTIALS


class Transaction:
    
    
    def get_transaction(store_id):
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                port=CREDENTIALS['PORT'],
                                database=CREDENTIALS['DATABASE'],
                                user=CREDENTIALS['USER'],
                                password=CREDENTIALS['PASSWORD']
                                )
            c = db.cursor()
            c.execute(f'SELECT * FROM bought WHERE store={store_id}')
            data = c.fetchall()
            
            items = []
            
            for col in data:
                transactions = {
                    "trabs_id": col[0],
                    "date": col[2],
                    "custnum": col[3],
                    "bnum": col[4],
                    "price": col[5],
                    "quantity": col[6],
                }
                items.append(transactions)
                
            res = {
                "store_id": store_id,
                "items": items,
            }
            
            c.close()
            db.close()
            
            return res
        
        except (psycopg2.Error, psycopg2.DatabaseError) as err:
            c.close()
            db.close()
            return f'Error while connecting to PostgreSQL Database: {err}'
    
    