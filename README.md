# Recommendation-Engine
HERKANSING Recommendation Engine - Opdracht 3 - 

- in de filter db word document zitten 2 screenshots met de querys.

2 nieuwe tables worden aangemaakt in table_create_sql.py
content_filter en collab_filter

Content filtering algoritme:

1. Zoekt naar ids van bezoekers
2. kijkt naar eerder bekeken.
3. zoekt naar gelijkzijnde producten gebaseerd op de regels: brand, categorie, gender en sub_category.
4. voegt producten die door de filter heen komen toe.

Collab filter algoritme:

1. Zoekt naar ids van bezoekers
2. kijkt naar eerder bekeken producten
3. zoekt naar de categorie van product
4. zoekt naar andere klanten met dezelfde categorie in content filter table
5. recommend de recommendation lijst van een ander klant met dezelfde categorie interesse
