import psycopg2
from config import CREDENTIALS

class Stock:
  def edit_stock(store_id, book_id, qty):
        
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
                      UPDATE stock
                      SET quantity={qty}
                      WHERE book_number={book_id} AND store_id={store_id};
                      
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