#!/usr/bin/env python

import MySQLdb as msql 
import pandas as pd 
import numpy as np 
import itertools
import json
import sys  
reload(sys)  
sys.setdefaultencoding('utf-8')

#mysql -u muna -h54.172.94.83 -p1469621300 opensooq_main -A

db = msql.connect("54.172.94.83", 'muna', '1469621300', 'opensooq_main', charset='utf8', use_unicode=True)
csr = db.cursor()
qry = "SELECT id, title, description, categories_id, subcategories_id FROM posts WHERE record_insert_date < '2016-8-20' LIMIT 100"
csr.execute(qry)
data = csr.fetchall()
def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    print type(desc)
    return [dict(itertools.izip([col[0] for col in desc], row)) 
            for row in data]
results = dictfetchall(csr)
catIds =  [1253,1729 ,1749 ,1775 ,1795 ,1817 ,1837 ,2265 ,2325 ,2383 ,2443 ,2501 ,2581 ,2661 ,2719 ,2779 ,2839 ,2897,2979 ,3955]
n = len(results)
for i in range(0, n):
	results[i]['catName'] = 'cars' if (results[i]['categories_id'] in catIds) else 'ow'
with open('posts.json', 'wb') as outf:
    json.dump(results, outf, ensure_ascii=False)

db.close()