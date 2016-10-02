#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
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
qry = "SELECT id, title, description, categories_id, subcategories_id FROM posts WHERE record_insert_date < '2016-8-20' LIMIT 2"
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
    
sr = "<p>\r\n\tتويوتا - \ أوريون - 2007 -., كامل المواصفات - عاد جلد - Toyota - Aurion - 2007 - - - 55836333 - 97799083</p>\r\n"
sr = "<p>\r\n\tميتسوبيشي - باجيرو - 2012 - اوتوماتيك كاملة، تكييف، المكابح المانعة للانغلاق مع نظام توزيع الكتروني لقوة الفرملة، عجلات قيادة ألية، نوافذ ألية، قفل ابواب مركزي، مصابيح امامية لمقاومة الضباب، دواسة جانبية، مراه معاكسة خلفيه للنهار والليل ، محدد السرعة، اي ام واف ام ، سي دي. صفر فوائد لمدة ثلاث سنوات - Mitsubishi - Pajero - 2012 - - V6,3.8L,ABS,Dual Airbags,Cruise Control,Alloy wheels,towing hooks, AM/FM with C.D player ,Key less entry, Auto side mirror 0% Free Interest for 3 years - 24743022 - 24715011</p>\r\n"
sr = re.sub(r'[\.\,\:\/\-\+\=\(\)0-9\<\>\n\t\r\\]', '', sr)
sr = re.sub(ur'( ال*)', u' ', sr)
sr = re.sub(ur'( لل*)', u' ', sr)
sr = re.split(u' ', sr)
print sr

db.close()