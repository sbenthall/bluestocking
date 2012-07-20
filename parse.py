import doxament

from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.corpus import stopwords
from itertools import combinations

            
class Document:
    text = ''

    def __init__(self,text):
        self.text = text

    def __str__(self):
        return self.text

    def to_dox(self):
        return doxament.Doxament(Parser(self).parse_relations())    


class Parser:
    doc = ''

    # initialize with a Document
    def __init__(self, doc):
        self.doc = doc

    def preprocess(self):
        # part of speech
        # chunking
        # pronoun resolution
        return "?"

    def parse_relations(self):
        sentence_tokenizer = PunktSentenceTokenizer()
        sentences = sentence_tokenizer.sentences_from_text(self.doc.text)

        relations = []
        for sentence in sentences:            
            relations.extend(self.parse_sentence(sentence))

        return relations

    def parse_sentence(self,sentence):
            sentence = self.neg_scope(sentence)
            tokens = [w for w in sentence if w.lower() not in stopwords.words("english")]
            pairs = combinations(tokens,2)
            relations = [self.make_relation(p) for p in pairs]
            return relations

    def make_relation(self,pair):
        co = True
        item1,item2 = self.strip_neg(pair[0]),self.strip_neg(pair[1])

        if self.is_neg(item1):
            item1 = self.strip_neg(item1)
            co = co

        if self.is_neg(item2):
            item2 = self.strip_neg(item2)
            co = not co

        return Relation(co,item1,item2)

    def strip_neg(self,word):
        if word[0:4] == "neg_":
            return word[4:]
        else:
            return word

    def is_neg(self,word):
        return word[0:4] == "neg_"

    def neg_scope(self, sentence):
        neg_words = ['not','never', 'isn\'t','was\'nt','hasn\'t']
        sentence = sentence.split()
        for ii in xrange(len(sentence)):
            if sentence[ii] in neg_words:
            #should really go to next punctuation pt, complementizer(?), clause-boundary 
                for jj in range(ii+1,len(sentence)):
                    sentence[jj] = 'neg_%s' % sentence[jj]
        
        return sentence


class Relation:
    co = True
    item1 = ''
    item2 = ''

    def __init__(self,co,item1,item2):
        self.co = co
        self.item1 = item1
        self.item2 = item2

    def flip(self):
        return Relation(not self.co, self.item1, self.item2)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
