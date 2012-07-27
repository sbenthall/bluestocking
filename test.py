import doxament
import parse
import random
import unittest

class TestParserMethods(unittest.TestCase):
    parser = None

    def setUp(self):
        text2 = "Ice cream is good.  Spinach is bad. Today was not bad."
        doc2 = parse.Document(text2)
        self.parser = parse.Parser(doc2)

    def test_make_relation(self):
        r1 = self.parser.make_relation(("neg_foo","bar"))
        self.assertTrue(not r1.co)

    def test_strip_neg(self):
        self.assertTrue(self.parser.strip_neg("neg_foo") == "foo")

    def test_is_neg(self):
        self.assertTrue(self.parser.is_neg('neg_foo'))


# GOLF_DIR = "tests/golf/"
# g1_doc = Document(open(GOLF_DIR + "g1.txt",'r').read())
# g2_doc = Document(open(GOLF_DIR + "g2.txt",'r').read())

# print "Golf Document 1: \n", g1_doc
# print "Golf Document 2: \n", g2_doc
# print compare_docs(g1_doc,g2_doc)

class GeneralTests(unittest.TestCase):
    def setUp(self):
        self.text1 = "Today was a good day.  Yesterday was a bad day."
        self.text2 = "Ice cream is good.  Spinach is bad. Today was not bad."


        doc1 = parse.Document(self.text1)
        doc2 = parse.Document(self.text2)

        self.dox1 = doc1.to_dox()
        self.dox2 = doc2.to_dox()
        self.kb = doxament.merge(self.dox1, self.dox2)

    def test_queries(self):

        print "Knowledge base documents"
        print self.text1
        print self.text2

        print "Query document 1"
        self.text3 = "Today was a good day because I ate ice cream."
        self.dox3 = parse.Document(self.text3).to_dox()
        print self.text3
        print "Consistency score:", self.kb.query(self.dox3)
        self.assertTrue(self.kb.query(self.dox3)[0] > 0)

        print "Query document 2"
        self.text4 = "Yesterday was good because I ate spinach. Today was bad."
        self.dox4 = parse.Document(self.text4).to_dox()
        print self.text4
        print "Consistency score:", self.kb.query(self.dox4)
        self.assertTrue(self.kb.query(self.dox4)[0] < 0)

        print "Query document 3"
        self.text5 = "Today was not good.  Ice cream is not good. Spinach is bad. I hate everything."
        self.dox5 = parse.Document(self.text5).to_dox()
        print self.text5
        print "Consistency score:", self.kb.query(self.dox5)

if __name__ == '__main__':
    unittest.main()
