from doxament import *

text1 = "Today was a good day.  Yesterday was a bad day."
text2 = "Ice cream is good.  Spinach is bad. Today was not bad."
text3 = "Today was a good day because I ate ice cream."
text4 = "Yesterday was good because I ate spinach. Today was bad."

doc1 = Document(text1)
doc2 = Document(text2)

dox1 = Doxament(doc1.parse_relations())
dox2 = Doxament(doc2.parse_relations())

kb = merge(dox1, dox2)

dox3 = Doxament(Document(text3).parse_relations())
dox4 = Doxament(Document(text4).parse_relations())

print "Knowledge base documents"
print text1
print text2
print "Query document 1"
print text3
print "Consistency score:", kb.query(dox3)
print "Query document 2"
print text4
print "Consistency score:", kb.query(dox4)