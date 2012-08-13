import doxament
import parse
import random
import unittest
import nltk
from pprint import pprint as pp
from parse import Chunkerator, ClauseChunkerator

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

#   def test_chunk_integration(self):
#       textchunk = "I am the man."
#       doc2 = parse.Document(textchunk)
#       self.parser = parse.Parser(doc2)
#       ps = self.parser.preprocess([textchunk])
#       self.assertTrue('the_man' in ps)


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


class TestChunkerator(unittest.TestCase):

   def test_find_chunks(self):
       rules = """
           NP: {<DT>?<JJ>*<NN.*>}
           NP: {<PRP>}
       """
       c = Chunkerator(rules, True)
       textChunk = 'I hate yellow snow because I know the black dogs are the ones who make the stuff.'
       textChunk = textChunk.split()
       outsent = c.chunk_sent(textChunk)
       print c.chunksSeen
       self.assertTrue(len(c.chunksSeen) == 5)

   def test_chunked_in_output(self):
       rules = """
           NP: {<DT>?<JJ>*<NN.*>}
           NP: {<PRP>}
       """
       c = Chunkerator(rules,True)
       textChunk = 'I hate yellow snow because I know the dogs are the ones who make the nasty stuff.'
       textChunk = textChunk.split()
       outsent = c.chunk_sent(textChunk)
       self.assertTrue('dogs' in outsent)

   def test_clause_chunker(self):
        rules = """
               NP: {<DT>?<JJ>*<NN.*>}
               NP: {<PRP>}
           """
        c = Chunkerator(rules,True)
        clauses = ClauseChunkerator(c)
        textChunk = 'Men fried potatoes and women fried onions.'
        outsent = clauses.chunk_sent(textChunk.split())
        self.assertTrue(len(outsent)==3)
        self.assertTrue('women_fried_onions.' in outsent)
        
        
if __name__ == '__main__':
    unittest.main()
