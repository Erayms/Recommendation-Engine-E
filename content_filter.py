
import psycopg2
import ast

# vul je eigen gegevens in van de sql database, !verander alleen de database en wachtwoord!
con = psycopg2.connect(
    host='localhost',
    port = '5433',
    database='huwebshop',
    user='postgres',
    password='O13o13o13!')

cur = con.cursor()

""" 'Content-Based Filtering:
        This is based on items liked by the customer and keywords used to describe the items. It also takes into consideration the preferences chosen by the customer'

Hier hou ik rekening met wat een bezoeker heeft bekeken, wat er op lijkt en voeg die product id's samen toe om die te kunnen recommenden."""

# informatie pakken van het laatst bekeken product
def viewed_info(id):
    cur.execute('''SELECT brand, category, gender, sub_category FROM products
    WHERE _id = %s
    ''',[id])
    result = cur.fetchall()
    return result

# Id's pakken van producten met dezelfde merk, category, gender en sub_category.
# aantal_pakken is tot hoeveel producten je zou willen pakken.
def similar(info, aantal_pakken):
    if len(info) < 1:
        return []

    ids = []
    cur.execute('''SELECT _id FROM products WHERE brand = %s and category = %s and gender = %s and sub_category = %s 
    ''',[info[0][0], info[0][1], info[0][2], info[0][3]])
    result = cur.fetchall()
    for i in result[:aantal_pakken]:
        ids.append(i[0])

    return ids, [info[0][1], info[0][2]]

def viewed_before(id):
    cur.execute('''SELECT recommendations FROM profiles
    WHERE _id = %s
    ''',[id])
    result = cur.fetchall()
    # alleen recommendations pakken die niet leeg zijn.
    return(ast.literal_eval(result[0][0])['viewed_before'])

def personalised_recommendations(id):
    v = viewed_before(id)
    if len(v) > 0:
        sim = similar(viewed_info(v[-1]), 6)
        if sim:
            personal_recom_list = sim[0]
            return personal_recom_list, sim[1]
    return []

def category_gender(product):
    cur.execute('''SELECT category, gender FROM products 
    WHERE _id = %s
    ''',[product])
    cat_gen = cur.fetchone()
    return cat_gen

# Zoekt producten met specifieke preferences van een bezoeker/klant en een product welke bekeken is.
# Ook worden lege recommendation listen eruit gefilterd.
def content_filter():
    all_recommendations = []

    cur.execute(f"SELECT _id FROM profiles WHERE recommendations <> ''")
    r = cur.fetchall()
    for customer in r:
        personalized_info = personalised_recommendations(customer[0])
        if len(personalized_info) > 1:
            all_recommendations.append([customer, personalized_info[0], personalized_info[1]])

    return all_recommendations

def insert_recommend(all_recom):
    for custo in all_recom:
        cur.execute("insert into content_filter (_id, recommend_ids, category, gender) values (%s, %s, %s, %s)", (custo[0][0], custo[1], custo[2][0], custo[2][1]))
        con.commit()

recommends = content_filter()
insert_recommend(recommends)

con.close()