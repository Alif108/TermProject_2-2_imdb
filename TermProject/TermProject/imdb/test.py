import random
import cx_Oracle
import base64

dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
c = conn.cursor()

movie_list = []

# query = """ SELECT "Title", "Photo" FROM IMDB.MOVIE WHERE UPPER("Title") LIKE UPPER(CONCAT(CONCAT('%','in'), '%'))
#             UNION ALL
#             SELECT "Title", "Photo" FROM IMDB.SHOW WHERE UPPER("Title") LIKE UPPER(CONCAT(CONCAT('%','in'), '%'))    """                      ### JOIN
#
# c.execute(query)
#
# res = c.fetchall()
#
# for i in res:
#     title = i[0]
#     photo = i[1].read()
#
#     encoded = base64.b64encode(photo)
#     encoded = encoded.decode('utf-8')
#
#     movie_list.append([title, encoded])
#
# for title, photo in movie_list:
#     print(title)
#     print(photo)

# for i in res:
#     title = i[0][0]
#     photo = i[0][1].read()
#     print(title)

#
# returnVal = c.var(int)

returnVal = c.callfunc("IMDB.MOVIE_EXISTS", int, [9])
print((returnVal))

conn.close()