allURL = []
indicator = "/forum?id="
prefix = "https://openreview.net"
with open("ICLR2018.html", "r") as f:
	
	allURL = []
	for line in f:
		if indicator in line:
			lst = line.split("\"")
			print(lst)
			for cand in lst:
				if indicator in cand and len(cand) > 10:
					allURL.append(prefix + cand)
with open("allURL2018.txt", "a") as w:
	for url in allURL:
		w.write(url + "\n")
