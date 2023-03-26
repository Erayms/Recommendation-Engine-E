from types import NoneType
import psycopg2
import ast

con = psycopg2.connect(
    host='localhost',
    port = '5433',
    database='huwebshop',
    user='postgres',
    password='O13o13o13!')

cur = con.cursor()

# hier word gekeken naar wat eerder bekeken is door de klant/bezoeker
def viewed_before(id):
    cur.execute('''select recommendations from profiles
    where _id = %s
    ''',[id])
    result = cur.fetchall()
    return(ast.literal_eval(result[0][0])['viewed_before'])

def category(product):
    cur.execute('''select category from products where _id = %s
        ''',[product])
    cat = cur.fetchone()
    return cat

# hier word naar de category gekeken van de bezoeker en recommend de 'recommendations' van klanten met dezelfde categorie in table content filter
def other_customer(id):
    v = viewed_before(id)
    if len(v) > 0:
        cat = category(v[0])
        cur.execute('''select recommend_ids from content_filter
        where category = %s
        ''',[cat])
        lst = cur.fetchall()
        return lst


# hier word de id van de bezoeker, en de recommendations van de een andere customer in table collab_filter gestopt.
def collab_filter():
    cur.execute(f"select _id from profiles where recommendations <> ''")
    r = cur.fetchall()
    for customer in r:
        rec = other_customer(customer[0])
        if rec and customer[0] != NoneType:
            cur.execute("insert into collab_filter (_id, recommend_ids) values (%s, %s)", (customer[0], rec[0][0]) )
            con.commit()

collab_filter()
con.close()