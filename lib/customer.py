import psycopg2

from config import CREDENTIALS


class Customer:
    
    def get_customers():
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                    port=CREDENTIALS['PORT'],
                                    database=CREDENTIALS['DATABASE'],
                                    user=CREDENTIALS['USER'],
                                    password=CREDENTIALS['PASSWORD']
                                    )
            c = db.cursor()
            c.execute(f"""
                      SELECT * FROM CUSTOMER
                      """)
            data = c.fetchall()
            msg = "success"
            
            items = []
            for col in data:
                customer = {
                    "customer_number": col[0],
                    "customer_name": col[1],
                    "street": col[2],
                    "city": col[3],
                    "state": col[4],
                    "country": col[5],
                }
                items.append(customer)
            
            if len(items) == 0:
                msg = "Not Found!"
                
            c.close()
            db.close()
            return items, msg
        
        except (psycopg2.Error, psycopg2.DatabaseError) as err:
            c.close()
            db.close()
            return [], f'Error while connecting to PostgreSQL Database: {err}'
            