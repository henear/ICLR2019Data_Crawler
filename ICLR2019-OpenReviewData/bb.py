#Problem        : Basic Encryption
#Language       : Python 3
#Compiled Using : py_compile
#Version        : Python 3.4.3
#Input for your program will be provided from STDIN
#Print out all output from your program to STDOUT

import sys

# data = sys.stdin.read().splitlines()
data = [5,14,13,12,11,10]

total = (int)(data[0])
curSum = 0
for i in range(1, len(data)):
    curSum += (int)(data[i])


if curSum % (total - 1) != 0:
    print("NO SOLUTION")
else:
    allNum = [0] * total
    allSum = curSum // (total - 1) 
    valid = True
    for i in range(total):
        curr = allSum - (int)(data[i+1])
        if curr >= 256 or curr < 0:
            valid = False
        allNum[i] = curr
    if valid:
        for data in allNum:
            print(data)
    else:
        print("NO SOLUTION")
