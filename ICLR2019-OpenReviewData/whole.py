import ai
import ai2
# B = ai2.crawlDateURL("urls.txt")
# print(B)
A = ai.crawl_meta("url2.txt")
B = ai2.crawlDateURL("url2.txt")
# print(A)
for i in range(len(A)):
	A[i][-3] = B[i][0]
	A[i][-2] = B[i][1]
	A[i][-1] = B[i][2]
keys = ["\"Title\"","\"Keyword\"","\"Rating1\"","\"Review1\"","\"Rating2\"","\"Review2\"","\"Rating3\"","\"Review3\"", "\"Abstract\"" ,"\"Publication_Date\"","\"Readers\"","\"URL\""]
with open("output.json", "a") as f:
	f.write("[\n")
	for j in range(len(A)):
		curLine = "{\n"
		for k in range(12):
			curLine += keys[k] + ": " + str(A[j][k]) + ",\n"
			# print(str(A[j][k]))
		curLine = curLine[:-2] + curLine[-1]
		if j < len(A) - 1:
			curLine += "},\n"
		else:
			curLine += "}\n"
		f.write(curLine)
	f.write("]")