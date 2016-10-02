#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import pandas as pd
import numpy as np 
import scipy as plt

post = {'title':'كيا سورينتو 2006', 'text':'مرخصة ومؤمنة سنة ـمحرك 3500 سي سي 6 سلندر دفع خلفي ـ بحالة جيدة جداً - شبابيك كهرباء - لون فيراني - مثبت سرعة - كراسي قماش - من المالك مباشرة - بسعر 12500 غير قابل للتفاوض للجادين' }
post2 = {'title':'شقة مفروشة للبيع بالرابية', 'text':'شقة مفروشة مميزة للبيع، بالرابية/الحي الدبلوماسي، تصلح لعائلة دبلوماسية،طابق اول، مساحتها 200م، 3 غرف نوم، واحد ماستر، 3 حمامات، صالون و سفرة، معيشة، برندتين، مطبخ راكب، مجهزة بجميع الاجهزة الكهربائية، 2 كندشن العقد سنوي ، للاستفسار: الاتصال على 07994424'}
def g(z):
	return 1/(1+exp(-z))

words = open('words.txt', 'r').readlines()
words = [i.replace('\n', '') for i in words]
n = len(words)
l = range(0, n)
#l = l[:len(words)]
words = {words[i]:i for i in l}
#words = 
# words.columns = ['KeyWds']
#words = pd.Series(range(0, len(words)), index=words)
# print words.count()
def parse(post, xlen=n):
    x = np.zeros([1, xlen+1])
    print x.size
    x[0][0] = 1
    wds = post['text'].split(' ') + post['title'].split(' ')
    wds = {i:1 for i in wds}
    for wd in wds:
        if wd in words:
            print wd
            x[0][words[wd]] = 1
#            print x

    return x
x = parse(post, n)
theta = np.ones([1, len(x[0])])
z = theta.dot(x.T)
print z
h = g(z)
print h

#x = pd.Series(x)
#theta = []
#z = x*
#h = g(z)