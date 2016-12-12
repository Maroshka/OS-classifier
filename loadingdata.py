#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import MySQLdb as msql 
import pandas as pd 
import numpy as np 
import itertools
import json
import sys  
from random import shuffle
reload(sys)  
sys.setdefaultencoding('utf-8')

#mysql -u muna -h54.172.94.83 -p1469621300 opensooq_main -A

db = msql.connect("54.172.94.83", 'muna', '1469621300', 'opensooq_main', charset='utf8', use_unicode=True)
csr = db.cursor()
catIds = "(1253,1729 ,1749 ,1775 ,1795 ,1817 ,1837 ,2265 ,2325 ,2383 ,2443 ,2501 ,2581 ,2661 ,2719 ,2779 ,2839 ,2897,2979 ,3955)"
reids = "(1262, 1347 ,1369, 1397, 1423, 1453, 1479, 1505, 1529, 1551, 1573, 1595, 1617, 1639, 1661, 1683, 2521, 2625, 2917, 3999)"

# realEstateIds = [1262, 1347 ,1369, 1397, 1423, 1453, 1479, 1505, 1529, 1551, 1573, 1595, 1617, 1639, 1661, 1683, 2521, 2625, 2917, 3999]
# qry = "SELECT id, title, description, categories_id, subcategories_id FROM posts WHERE categories_id in \
# (1253,1729 ,1749 ,1775 ,1795 ,1817 ,1837 ,2265 ,2325 ,2383 ,2443 ,2501 ,2581 ,2661 ,2719 ,2779 ,2839 ,2897,2979 ,3955) \
#  and record_insert_date < '2016-8-20' LIMIT 7000"

# qry2 = "SELECT id, title, description, categories_id, subcategories_id FROM posts WHERE categories_id not in \
# (1253,1729 ,1749 ,1775 ,1795 ,1817 ,1837 ,2265 ,2325 ,2383 ,2443 ,2501 ,2581 ,2661 ,2719 ,2779 ,2839 ,2897,2979 ,3955) \
#  and record_insert_date < '2016-8-20' LIMIT 6000"

# reqry = "SELECT id, title, description, categories_id, subcategories_id FROM posts WHERE categories_id in \
# (1262, 1347 ,1369, 1397, 1423, 1453, 1479, 1505, 1529, 1551, 1573, 1595, 1617, 1639, 1661, 1683, 2521, 2625, 2917, 3999) \
#  and record_insert_date < '2016-8-20' LIMIT 7000"
# csr.execute(qry)
# data = csr.fetchall()
# #csr2 = db.cursor()
# csr.execute(qry2)
# data2 = csr.fetchall()
def dictfetchall(cursor, data):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    print type(desc)
    return [dict(itertools.izip([col[0] for col in desc], row)) 
            for row in data]
# results = dictfetchall(csr, data)
# results2 = dictfetchall(csr2, data2)
# # catIds =  [1253,1729 ,1749 ,1775 ,1795 ,1817 ,1837 ,2265 ,2325 ,2383 ,2443 ,2501 ,2581 ,2661 ,2719 ,2779 ,2839 ,2897,2979 ,3955]
# n = len(results)
# m = len(results2)
# for i in range(0, n):
# 	results[i]['catName'] = 'CARS' 

# for i in range(0, m):
# 	results2[i]['catName'] = 'OW' 

# results = results + results2
# shuffle(results)
# with open('posts.json', 'wb') as outf:
#     json.dump(results, outf, ensure_ascii=False)

def loadData(ids, cat):
	db = msql.connect("54.172.94.83", 'muna', '1469621300', 'opensooq_main', charset='utf8', use_unicode=True)
	csr = db.cursor()
	qry = "SELECT id, title, description, categories_id, subcategories_id FROM posts WHERE categories_id in "+ids+" \
	 and record_insert_date < '2016-8-20' LIMIT 10000"

	qry2 = "SELECT id, title, description, categories_id, subcategories_id FROM posts WHERE categories_id not in "+ids+" \
	 and record_insert_date < '2016-8-20' LIMIT 10000"
	csr.execute(qry)
	data = csr.fetchall()
	csr.execute(qry2)
	data2 = csr.fetchall()
	results = dictfetchall(csr, data)
	results2 = dictfetchall(csr, data2)
	n = len(results)
	m = len(results2)
	for i in range(0, n):
		results[i]['catName'] = cat 

	for i in range(0, m):
		results2[i]['catName'] = 'OW'
	filename = cat+".json" 
	results = results + results2
	print len(results)
	shuffle(results)
	with open(filename, 'wb') as outf:
	    json.dump(results, outf, ensure_ascii=False)


cats = [(catIds,'CARS'), (reids,'REALESTATE')]
for cat in cats:
	loadData(cat[0], cat[1])

db.close()

