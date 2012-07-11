from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.corpus import stopwords
from itertools import combinations

class Doxament:
    relations = []

    def __init__(self, relations):
        self.relations = relations

    def query(self, qdox):
        '''
        Query the first doxament with the second
        doxament for consistency/coverage
        '''
        total = len(qdox.relations)
        found = 0
        contras = []
        
        for r in qdox.relations:
            found += 1 if r in self.relations else 0
            contra_rel = self.flip_polarity(r)
            if contra_rel in self.relations:
                contras.extend(contra_rel) 
                found -= 1

        score = float(found) / total
        return score, contras

    def flip_polarity(self,rel):
        return (not rel[0],rel[1],rel[2])

            
class Document:
    text = ''

    def __init__(self,text):
        self.text = text

    def __str__(self):
        return self.text

    def to_dox(self):
        return Doxament(self.parse_relations())

    def neg_scope(self, sentence):
        neg_words = ['not','never', 'isn\'t','was\'nt','hasn\'t']
        sentence = sentence.split()
        for ii in xrange(len(sentence)):
            if sentence[ii] in neg_words:
                #should really go to next punctuation pt, complementizer(?), clause-boundary 
                for jj in range(ii+1,len(sentence)):
                    sentence[jj] = 'neg_%s' % sentence[jj]
        
        return sentence
    

    def convert_to_negprop(self,pair):
        negated = False
        item1,item2 = self.strip_neg(pair[0]),self.strip_neg(pair[1])
        for x in pair:
            if x[0:4] == "neg_":
                negated = not negated
        return (negated,item1,item2)

    

    def strip_neg(self,word):
        if word[0:4] == "neg_":
            return word[4:]
        else:
            return word
    

    def parse_relations(self):
        sentence_tokenizer = PunktSentenceTokenizer()
        sentences = sentence_tokenizer.sentences_from_text(self.text)

        relations = []
        for sentence in sentences:
            sentence = self.neg_scope(sentence)
            tokens = [w for w in sentence if w.lower() not in stopwords.words("english")]
            pairs = combinations(tokens,2)
            relations.extend([tuple(pair) for pair in pairs])
        
        relations = [self.convert_to_negprop(rel) for rel in relations]

        return relations

def merge(dox1, dox2):
    r1 = list(dox1.relations)
    r2 = list(dox2.relations)
    r1.extend(r2)
    return Doxament(r1)

def compare_docs(doc1,doc2):
    dox1 = Doxament(doc1.parse_relations())
    dox2 = Doxament(doc2.parse_relations())

    return dox1.query(dox2)
