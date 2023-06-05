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
            
            res = []
            for col in data:
                staff = {
                    "staff_id": col[0],
                    "name": col[1],
                    "hire_date": col[2],
                    "address": col[3],
                    "sex": col[4],
                    "is_manager": col[5],
                }
                res.append(staff)
            
            c.close()
            db.close()
            
            return res
        
        except (psycopg2.Error, psycopg2.DatabaseError) as err:
            c.close()
            db.close()
            return f'Error while connecting to PostgreSQL Database: {err}'
    
    