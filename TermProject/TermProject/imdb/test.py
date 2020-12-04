import random
import cx_Oracle
import base64

dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
c = conn.cursor()

movie_list = []

# query = """ SELECT S."sID",S."Title", 0
#                 FROM SHOW S, DIRECTOR D, DIRECTOR_SHOW DS
#                 WHERE UPPER(D."Name") LIKE UPPER('christopher nolan')
#                 AND D."dID" = DS."dID"
#                 AND S."sID" = DS."sID"
#                 UNION
#                 SELECT M."mID",M."Title", 1
#                 FROM MOVIE M, DIRECTOR D, DIRECTOR_MOVIE DM
#                 WHERE UPPER(D."Name") LIKE UPPER('christopher nolan')
#                 AND D."dID" = DM."dID"
#                 AND M."mID" = DM."mID" """                      ### JOIN

# query = """  SELECT M."mID", M."Title", AM."role", 1
#                 FROM MOVIE M, ARTIST A, ARTIST_MOVIE AM
#                 WHERE UPPER(A."Name") LIKE UPPER('LeoNardo Dicaprio')
#                 AND A."aID" = AM."aID"
#                 AND M."mID" = AM."mID"
#                 UNION
#                 SELECT S."sID", S."Title", ASW."role", 0
#                 FROM SHOW S, ARTIST A, ARTIST_SHOW ASW
#                 WHERE UPPER(A."Name") LIKE UPPER('LeoNardo Dicaprio')
#                 AND A."aID" = ASW."aID"
#                 AND S."sID" = ASW."sID"   """

query = """  SELECT D."Name", D."dID", 0 
                        FROM DIRECTOR D, DIRECTOR_SHOW DS
                        WHERE DS."sID" = 5
                        AND DS."dID" = D."dID"   """

c.execute(query)

res = c.fetchall()

for x,y,z in res:
    print(x,y,z)

# for i in res:
#     id = i[0]
#     title = i[1]
#     # photo = i[2].read()
#     choice = i[2]
#
#     # encoded = base64.b64encode(photo)
#     # encoded = encoded.decode('utf-8')
#
#     movie_list.append([id, title, choice])
#
# for x in movie_list:
#     # print(id)
#     # print(title)
#     # print(choice)
#     print(x)

# for i in res:
#     title = i[0][0]
#     photo = i[0][1].read()
#     print(title)

#
# returnVal = c.var(int)

# returnVal = c.callfunc("IMDB.MOVIE_EXISTS", int, [9])
# print((returnVal))

conn.close()