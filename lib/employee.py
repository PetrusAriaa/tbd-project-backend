import psycopg2

from config import CREDENTIALS


class Employee:
    
    
    def get_employees():
        try:
            db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                                port=CREDENTIALS['PORT'],
                                database=CREDENTIALS['DATABASE'],
                                user=CREDENTIALS['USER'],
                                password=CREDENTIALS['PASSWORD']
                                )
            c = db.cursor()
            c.execute('SELECT * FROM staff')
            data = c.fetchall()
            msg = "success"
            
            items = []
            for col in data:
                staff = {
                    "staff_id": col[0],
                    "name": col[1],
                    "hire_date": col[2],
                    "address": col[3],
                    "sex": col[4],
                    "is_manager": col[5],
                }
                items.append(staff)
            
            if len(items) == 0:
                msg = "Not Found!"
            
            c.close()
            db.close()
            
            return items, msg
        
        except (psycopg2.Error, psycopg2.DatabaseError) as err:
            c.close()
            db.close()
            return [], f'Error while connecting to PostgreSQL Database: {err}'
    
    