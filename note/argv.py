import sys
import difflib

#print sys.argv[0],sys.argv[1]
d = difflib.HtmlDiff()
with open(sys.argv[1],'rb') as f:
	text1 = f.readlines()
	#print text1
with open(sys.argv[2],'rb') as f:
	text2 = f.readlines()
	#print text2

print d.make_file(text1,text2)