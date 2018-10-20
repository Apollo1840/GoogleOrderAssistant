from bc2 import BasicCrawler
import pandas as pd
import math
import time
import random

import re
import sys

#print(top_tags)
#for i in top_tags.find_all('li'):
#	print(i.text)

def get_top_n_tags(data, n):

	top_tags = [e.text for e in data.find('ul', class_ ='oc-reviews-0cfa0da3').find_all('li')]
	return top_tags[:3] + top_tags[4:n+1]


def get_additional(data, tags=[]):
	res = {t : "" for t in tags}
	for e in data.find_all('div', class_='_1e864f49'):
		attribute = e.find('span')
		if attribute.text in tags:
			attribute_val = e.find('div', class_='_16c8fd5e _1f1541e1')
			if attribute_val != None:
				res[attribute.text] = attribute_val.text
	return res


bc = BasicCrawler()
res = bc.get_soup(sys.argv[1])

print(get_additional(data=res, tags=["Additional", "Cuisines", "Dining Style"]))

#print(get_top_n_tags(res, 7))