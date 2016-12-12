#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import pandas as pd
import numpy as np 
import scipy as plt
import re
import nltk
import json
import string
import statsmodels.discrete.discrete_model as sm
from patsy import *
from sklearn.linear_model import LogisticRegression
from random import shuffle
from sklearn.metrics import classification_report
from gui import *
from Tkinter import *

"""Loading Data into json file """

def dfbuilder(feats):
	x = []
	with open(feats, 'r') as features:
		for word in features:
			x.append(word.replace('\n', ''))
	# print len(x)
	if '' in x:
		x.remove('')
	x = list(set(x))
#	print len(x)
	df = {wd:[1] for wd in x}
#	print len(df)
	df = pd.DataFrame(df)
	df.loc[:,'Y'] = [1]
#	print len(df.columns)
	return x, df

def dfiller(post, x):
	row = [int(wd in post) for wd in x]
	row.append(int('CARS' in post)) 
	return row

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

def load(jsonf, cat):
	with open(jsonf) as data_file:
		data = json.load(data_file)
#	print len(data)
	posts = []
	for i in range(0, len(data)):
#		print i
		tokens = clean(data[i]['description'])
		if data[i]['catName'] != cat:
			tokens.append('OW')
		else:
			tokens.append(cat)
		posts.append(tokens)
		# print tokens[0]

	return posts

"""Modeling"""
#df_train = df.iloc[:1300,:]
#df_test = df.iloc[1330:, :]
#formula = 'Y ~ '
#for col in df.columns:
#	if col != df.columns[-1]:
#		formula = formula + col + ' + '
#	else:
#		formula = formula + col
#
#y_train, x_train = dmatrices(formula, data = df_train, return_type='dataframe')
#y_test, x_test = dmatrices(formula, data = df_test, return_type='dataframe')
#model = st.Logit(y_train,x_train)
#res = model.fit()
#print res.summary()
# 
def formulate(df, y):
	st = ''
	for col in df.columns:
		if col != df.columns[-1]:
			st = st + "Q('"+col+"')" + ' + '
		else:
			st = st + "Q('"+col+"')"  +''
	formula = y+" ~ "+ st

	return formula

def modelaway(df, x, jsonf):
	catname = jsonf.replace('.json', '')
	posts = load(jsonf, catname)
	print len(posts)
     
	for i in range(0, len(posts)):
#		print len(dfiller(posts[i], x))
#		print len(df.columns)
		df.loc[i] = dfiller(posts[i], x)

	df_train = df.iloc[:10000,:]
	df_test = df.iloc[10000:, :]
	formula = formulate(df, 'Y')
	y_train, x_train = dmatrices(formula, data = df_train, return_type='dataframe')
	y_test, x_test = dmatrices(formula, data = df_test, return_type='dataframe')
	model = LogisticRegression()
	res = model.fit(x_train, y_train)
	y_pred = model.predict(x_test)
	print y_pred[:10]
	print y_test[:10]
	print classification_report(y_test, y_pred)


def main(df, x, jsonl):
	# posts = load('posts.json')
	# test = load('tests.json')
	for jsonf in jsonl:
		modelaway(df, x, jsonf)

	

def sqlQry(id):
	qry = "SELECT id, title, description, categories_id, subcategories_id FROM posts WHERE id ="+id
	csr.execute(qry)
	data = csr.fetchall()
	result = dictfetchall(csr, data)
	result[0]['catName'] = 'CARS' if result[0]['categories_id'] in catIds else 'OW'

	return result

def classify2(id, df, x, model, s):
	post = sqlQry(id)
	cat = post[0]['catName']
	post = clean(post[0]['description'])
	post.append(cat)
	df.loc[0] = dfiller(post, x)
	# df.drop('Y', 1)
	formula = formulate(df, 'Y')
	y_actual, x_exp = dmatrices(formula, data = df, return_type='dataframe')
	y_pred = model.predict()
	cat = 'Cars' if y_pred else 'ow'
	s.set(cat)



 
def gui(model, df, x):
	hwtext = Label(top, text = "Enter the post id here, mf:")
	hwtext.pack(side='left')

	r = StringVar()
	r.set('0')

	entry = Entry(top, width=12, textvariable=r)
	entry.pack(side='left')
	s = StringVar()
	btn = Button(top, width=6, text='Classify', command=lambda: classify(r.get(), df, x, model, s))
	btn.pack(side='left')

	result = Label(top, width=6, textvariable=s)
	result.pack(side='left')

	root.mainloop()

if __name__ == '__main__':
	x, df = dfbuilder('features.txt')
	main(df, x, ['CARS.json', 'REALESTATE.json'])
	# gui(model, df, x)

