import requests
from bs4 import BeautifulSoup
import time

def crawlDateURL(allURLs):
	urls = []
	with open(allURLs) as f:
		urls = f.readlines()
	urls = [url.strip() for url in urls]
	b = []
	for url in urls:
		response = requests.get(url)
		soup = BeautifulSoup(response.text, "html5lib")

		metas = soup.find_all('meta')

# print( [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'citation_publication_date' ])
	
		a = [""] * 3
		for meta in metas:
	
			if "name" in meta.attrs:
		
				if meta.attrs["name"] == "citation_publication_date":
					a[0] = "\"" + (meta.attrs["content"] ) + "\""
				if meta.attrs["name"] == "citation_pdf_url":
					a[2] = "\"" +(meta.attrs["content"] ) + "\""
		

		# spans = soup.find_all('span')
		t = soup.find_all("span",{"class": "item"})
		for tt in t:
			ttt = str(tt)
			if "readers:" in ttt:
				print(ttt)
				c, d = ttt.split(":")
				e, f = d.split("<")
				a[1] = "\"" + e[1:] + "\""
		print(a)
		b.append(a)
		
	print(b)
	return b

crawlDateURL("url2.txt")



# for span in spans:
# 	if "item" in span.attrs:
# 		print("h")