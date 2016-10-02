import re

def clean (post):
	"""the input is a dict of title, description and category"""
	pass
class clean(object):
	"""docstring for clean"""
	def __init__(self, post):
		super(clean, self).__init__()
		self.arg = arg
		self.text = post['title'] +' '+ post['description']
		# self.title = post['title']
		self.cat = post['catName'] 

	def rmpun(self):
		self.text = self.text.lower()
		self.text = re.sub(r'[\.\,\:\/\-\+\=\(\)0-9\<\>\n\t\r\%\$]' ,u'',self.text)
		re.sub(r'[\.\,\:\/\-\+\=\(\)0-9\<\>\n\t\r\\]', '', self.text)
		self.text = re.sub(ur'( ال*)', u' ', self.text)
		self.text = re.sub(ur'( لل*)', u' ', self.text)

	def remdef(self, post):
		pass

		