import random
import cx_Oracle

dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
cur = conn.cursor()

query = """ SELECT "mID" FROM 
                    IMDB.MOVIE WHERE "mID" = (:mID) """

cur.execute(query, {'mID': 9})

res = cur.fetchall()

print(len(res))