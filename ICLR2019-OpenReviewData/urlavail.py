import requests
prefix = "https://openreview.net/forum?id="
# request = requests.get('http://www.cs.utexas.edu/~henear/picture/zhangzhe/19960317.png')
# if request.status_code == 200:
#     print('Web site exists')
# else:
#     print('Web site does not exist') 

with open("myurls.txt", "a") as f:
	for a in range(256):
		for b in range(256):
			for c in range(256):
				for d in range(256):
					for e in range(256):
						for f in range(256):
							for g in range(256):
								for h in range(256):
									for i in range(256):
										for j in range(256):
											postfix = chr(a) + chr(b) + chr(c) + chr(d) + chr(e) + chr(f) + chr(g) + chr(h) + chr(i) + chr(j)
											request = requests.get(prefix + postfix)
											if request.status_code == 200:
												f.write(request)