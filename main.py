#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import pandas as pd
import numpy as np 
import scipy as plt
import re
import nltk
import string
import statsmodels.discrete.discrete_model as sm
from patsy import *
from sklearn.linear_model import LogisticRegression
from random import shuffle
from sklearn.metrics import classification_report
import re
import MySQLdb as msql 
import itertools
import json
import sys  
from random import shuffle
from urllib2 import *
from bs4 import BeautifulSoup

reload(sys)  
sys.setdefaultencoding('utf-8')

"""Loading Data into json file """

class Classifier(object):
	"""docstring for Classifier"""
	def __init__(self, feats, ids, cat):
		super(Classifier, self).__init__()
		self.ids = ids
		self.feats = feats
		self.cat = cat

	@staticmethod
	def dictfetchall(cursor, data):
#    """Returns all rows from a cursor as a list of dicts"""
	    desc = cursor.description
	    print type(desc)
	    return [dict(itertools.izip([col[0] for col in desc], row)) 
	            for row in data]

	@staticmethod
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
		return filename

	@staticmethod	
	def dfbuilder(feats):
		x = []
		with open(feats, 'r') as features:
			for word in features:
				x.append(word.replace('\n', ''))
		if '' in x:
			x.remove('')
		x = list(set(x))
		df = {wd:[1] for wd in x}
		df = pd.DataFrame(df)
		df.loc[:,'Y'] = [1]
		return x, df

	@staticmethod
	def dfiller(post, x):
		row = [int(wd in post) for wd in x]
		row.append(int('CARS' in post)) 
		return row

	@staticmethod
	def clean(text):
		text = text.lower()
		text = re.sub(r'\<(\/|)[a-z](\>|)', u'',text)
		text = re.sub(r'[0-9]', u'', text)
		punc = string.punctuation + u'،'
		for k in punc:
			text = text.replace(k, '')  
		text = re.sub(r'\s+', ' ', text)
		tokens = text.split()

		return tokens

	@staticmethod
	def load(jsonf, cat):
		with open(jsonf) as data_file:
			data = json.load(data_file)
		posts = []
		for i in range(0, len(data)):
			tokens = Classifier.clean(data[i]['description'])
			if data[i]['catName'] != cat:
				tokens.append('OW')
			else:
				tokens.append(cat)
			posts.append(tokens)

		return posts

	@staticmethod
	def formulate(df, y):
		st = ''
		for col in df.columns:
			if col != df.columns[-1]:
				st = st + "Q('"+col+"')" + ' + '
			else:
				st = st + "Q('"+col+"')"  +''
		formula = y+" ~ "+ st

		return formula

	@staticmethod
	def modelaway(df, x, jsonf):
		catname = jsonf.replace('.json', '')
		posts = Classifier.load(jsonf, catname)
		print len(posts)
	     
		for i in range(0, len(posts)):
			df.loc[i] = Classifier.dfiller(posts[i], x)

		df_train = df.iloc[:10000,:]
		df_test = df.iloc[10000:, :]
		formula = Classifier.formulate(df, 'Y')
		y_train, x_train = dmatrices(formula, data = df_train, return_type='dataframe')
		y_test, x_test = dmatrices(formula, data = df_test, return_type='dataframe')
		model = LogisticRegression()
		model = model.fit(x_train, y_train)
		y_pred = model.predict(x_test)
		print y_pred[:10]
		print y_test[:10]
		print classification_report(y_test, y_pred)
		return model


	def main(self):
		x, df = Classifier.dfbuilder(self.feats)
		print len(df)
		dfx = df
		xx = x
		# jsonf = Classifier.loadData(self.ids, self.cat)
		jsonf = 'CARS.json'
		model = Classifier.modelaway(df, x, jsonf)
		self.model = model
		return model, dfx, xx

	@staticmethod
	def crawl(id):
		url = 'https://jo.opensooq.com/ar/search/'+str(id)
		html = urlopen(url)
		page = BeautifulSoup(html)
		desc = page.find('div', {'class':'postDesc'}).text
		return desc

	def predict(self, id, model, df,x):
		desc = Classifier.crawl(id)
		tokens = Classifier.clean(desc)
		df.loc[0] = Classifier.dfiller(tokens, x) 
		formula = Classifier.formulate(df, 'Y')
		nth, x_pred = dmatrices(formula, data = df, return_type='dataframe')
		y = model.predict(x_pred)
		return y



if __name__ == '__main__':
	catIds = "(1253,1729 ,1749 ,1775 ,1795 ,1817 ,1837 ,2265 ,2325 ,2383 ,2443 ,2501 ,2581 ,2661 ,2719 ,2779 ,2839 ,2897,2979 ,3955)"
	model = Classifier('features.txt',catIds, 'CARS')
	mdl, df, x = model.main()
	id = 47635055
	y = model.predict(id, mdl, df, x)