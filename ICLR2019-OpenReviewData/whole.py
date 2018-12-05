import ai
import ai2
# B = ai2.crawlDateURL("urls.txt")
# print(B)
A = ai.crawl_meta("url2018oral.txt")
B = ai2.crawlDateURL("url2018oral.txt")
# print(A)
for i in range(len(A)):
	A[i][-3] = B[i][0]
	A[i][-2] = B[i][1]
	A[i][-1] = B[i][2]
keysfromA = ["\"Title\"","\"Keyword\"","\"Rating1\"","\"Review1\"","\"Rating2\"","\"Review2\"","\"Rating3\"","\"Review3\"", "\"Abstract\""]
keysfromB = ["\"Publication_Date\"","\"Readers\"","\"URL\""]
with open("output2018oral.json", "a") as f:
	f.write("[\n")
	for j in range(len(A)):
		curLine = "{\n"
		for k in range(9):
			curLine += keysfromA[k] + ": " + str(A[j][k]) + ",\n"
			if "Review" in keysfromA[k]:
				curID = (int)(keysfromA[k][-2:-1])
				
				cmtidx = -curID - 3
				if A[j][cmtidx] != '':
					for cmt in range(len(A[j][cmtidx])):
						cmtkeys = "\"Comment" + str(curID) + str(cmt+1) + "\""
						cmtVals = A[j][cmtidx][cmt]
						curLine += cmtkeys + ": \"" + cmtVals + "\",\n"



		
		for k in range(3):
			curLine += keysfromB[k] + ": " + str(A[j][k - 3]) + ",\n"
		curLine = curLine[:-2] + curLine[-1]
		if j < len(A) - 1:
			curLine += "},\n"
		else:
			curLine += "}\n"
		f.write(curLine)
	f.write("]")