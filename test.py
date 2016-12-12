import itertools
import json
import sys  
from random import shuffle
reload(sys)  
sys.setdefaultencoding('utf-8')

db = msql.connect("54.172.94.83", 'muna', '1469621300', 'opensooq_main', charset='utf8', use_unicode=True)
csr = db.cursor()
catIds = [1253,1729 ,1749 ,1775 ,1795 ,1817 ,1837 ,2265 ,2325 ,2383 ,2443 ,2501 ,2581 ,2661 ,2719 ,2779 ,2839 ,2897,2979 ,3955]
qry = "SELECT id, title, description, categories_id, subcategories_id FROM posts WHERE  record_insert_date < '2016-8-20' LIMIT 5000"

csr.execute(qry)
data = csr.fetchall()

def dictfetchall(cursor, data):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    print type(desc)
    return [dict(itertools.izip([col[0] for col in desc], row)) 
            for row in data]
results = dictfetchall(csr, data)
catIds =  [1253,1729 ,1749 ,1775 ,1795 ,1817 ,1837 ,2265 ,2325 ,2383 ,2443 ,2501 ,2581 ,2661 ,2719 ,2779 ,2839 ,2897,2979 ,3955]
n = len(results)
for i in range(0, n):
	results[i]['catName'] = 'CARS' if results[i]['categories_id'] in catIds else 'OW'

with open('tests.json', 'wb') as outf:
    json.dump(results, outf, ensure_ascii=False)

db.close()

