import cx_Oracle


###READING THE BLOB FROM DATABASE...

dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='ORCL')
conn = cx_Oracle.connect(user='IMDB', password='imdb', dsn=dsn_tns)
cur = conn.cursor()

query = "SELECT * FROM IMDB.MOVIE"
m = cur.execute(query)

##FETCHING THE IMAGE AS BLOB
for items in m:
    image = items[6].read()                         #read() FUNCTION CONVERTS IT FROM BLOB TO BYTES

##WRITING THE IMAGE(BYTES) TO A FILE

# with open('silence.png','wb') as f:
#      f.write(image)

cur.close()

