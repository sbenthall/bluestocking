import doxament
import parse
import random
import unittest
from pprint import pprint as pp

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
        print "Knowledge base relations"
        pp(self.kb.relations)

        self.counter = 1
        def query(text,kb):
            print "Query document %d" % (self.counter)
            self.counter += 1
            dox = parse.Document(text).to_dox()
            print text
            q = kb.query(dox)
            print "Query result:"
            print q
            return q

        self.assertTrue(query("Today was a good day because I ate ice cream.", self.kb)[0] > 0)

        self.assertTrue(query("Yesterday was good because I ate spinach. Today was bad.",self.kb)[0] < 0)

        self.assertTrue(doxament.Relation(False,'Today','good') in query("Today was not good.  Ice cream is not good. Spinach is bad. I hate everything.",self.kb)[1])

        self.assertTrue(query("Yesterday was good.  Spinach is good.",self.kb)[0] < 0)

if __name__ == '__main__':
    unittest.main()
