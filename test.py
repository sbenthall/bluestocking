from doxament import *
from parse import Document

text1 = "Today was a good day.  Yesterday was a bad day."
text2 = "Ice cream is good.  Spinach is bad. Today was not bad."
text3 = "Today was a good day because I ate ice cream."
text4 = "Yesterday was good because I ate spinach. Today was bad."
text5 = "Today was not good.  Ice cream is not good. Spinach is bad. I hate everything."

doc1 = Document(text1)
doc2 = Document(text2)

dox1 = doc1.to_dox()
dox2 = doc2.to_dox()

kb = merge(dox1, dox2)

dox3 = Document(text3).to_dox()
dox4 = Document(text4).to_dox()

print "Knowledge base documents"
print text1
print text2
print "Query document 1"
print text3
print "Consistency score:", kb.query(dox3)
print "Query document 2"
print text4
print "Consistency score:", kb.query(dox4)
print text5
print "Consistency score:", kb.query(Document(text5).to_dox())


# GOLF_DIR = "tests/golf/"
# g1_doc = Document(open(GOLF_DIR + "g1.txt",'r').read())
# g2_doc = Document(open(GOLF_DIR + "g2.txt",'r').read())

# print "Golf Document 1: \n", g1_doc
# print "Golf Document 2: \n", g2_doc
# print compare_docs(g1_doc,g2_doc)
