import psycopg2
from config import CREDENTIALS


class SQLBuilder:
  def start_query(req):
    try:
      db = psycopg2.connect(host=CREDENTIALS['HOSTNAME'],
                            port=CREDENTIALS['PORT'],
                            database=CREDENTIALS['DATABASE'],
                            user=CREDENTIALS['USER'],
                            password=CREDENTIALS['PASSWORD'])
      c = db.cursor()
      c.execute(f"{req['sql']}")
      data = c.fetchall()
      c.close()
      db.close()
      return data
    except (psycopg2.Error, psycopg2.DatabaseError) as err:
      c.close()
      db.close()
      return [], f'Error while connecting to PostgreSQL Database: {err}'