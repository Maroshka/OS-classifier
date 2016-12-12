from Tkinter import *
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
catIds = [1253,1729 ,1749 ,1775 ,1795 ,1817 ,1837 ,2265 ,2325 ,2383 ,2443 ,2501 ,2581 ,2661 ,2719 ,2779 ,2839 ,2897,2979 ,3955]
root = Tk()
top = Frame(root)
top.pack(side = 'top')

def classify():
	global s
	qry = "SELECT id, title, description, categories_id, subcategories_id FROM posts WHERE id ="+r.get()
	csr.execute(qry)
	data = csr.fetchall()
	s.set(type(r.get()))

hwtext = Label(top, text = "Enter the post id here, mf:")
hwtext.pack(side='left')

r = StringVar()
r.set('0')

entry = Entry(top, width=12, textvariable=r)
entry.pack(side='left')

btn = Button(top, width=6, text='Classify', command=classify)
btn.pack(side='left')

s = StringVar()

result = Label(top, width=6, textvariable=s)
result.pack(side='left')

root.mainloop()