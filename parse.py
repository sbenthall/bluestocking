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
            relations = [convert_to_negprop(rel) for rel in relations]

            return relations

    def parse_sentence(self,sentence):
            sentence = neg_scope(sentence)
            tokens = [w for w in sentence if w.lower() not in stopwords.words("english")]
            pairs = combinations(tokens,2)
            #should return type Relation[]
            return [tuple(pair) for pair in pairs]


def neg_scope(sentence):
    neg_words = ['not','never', 'isn\'t','was\'nt','hasn\'t']
    sentence = sentence.split()
    for ii in xrange(len(sentence)):
        if sentence[ii] in neg_words:
            #should really go to next punctuation pt, complementizer(?), clause-boundary 
            for jj in range(ii+1,len(sentence)):
                sentence[jj] = 'neg_%s' % sentence[jj]
        
    return sentence

def strip_neg(word):
    if word[0:4] == "neg_":
        return word[4:]
    else:
        return word

def convert_to_negprop(pair):
    negated = False
    item1,item2 = strip_neg(pair[0]),strip_neg(pair[1])
    for x in pair:
        if x[0:4] == "neg_":
            negated = not negated
    return (negated,item1,item2)


