import psycopg2

con = psycopg2.connect(
        host='localhost',
        port = '5433',
        database='huwebshop',
        user='postgres',
        password='O13o13o13!')
cursor = con.cursor()

# 2 nieuwe tables aanmaken voor recommendations
info = (
   '''
CREATE TABLE content_filter(
   _id varchar(100),
   recommend_ids text,
   category varchar(100),
   gender varchar(100)
   )
''',
'''
CREATE TABLE collab_filter(
   _id varchar(100),
   recommend_ids text
   )                     
''')

for x in info:
   cursor.execute(x)
con.commit()
con.close()