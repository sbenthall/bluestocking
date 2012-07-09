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
        for r in qdox.relations:
            found += 1 if r in self.relations else 0
            
        score = float(found) / total
        return score


class Document:
    text = ''

    def __init__(self,text):
        self.text = text

    def to_dox(self):
        return Doxament(self.parse_relations())

    def parse_relations(self):
        sentence_tokenizer = PunktSentenceTokenizer()
        sentences = sentence_tokenizer.sentences_from_text(self.text)

        relations = []
        for sentence in sentences:
            tokens = [w for w in sentence.split() if w.lower() not in stopwords.words("english")]
            pairs = combinations(tokens,2)
            relations.extend([tuple(pair) for pair in pairs])

        return relations

def merge(dox1, dox2):
    r1 = list(dox1.relations)
    r2 = list(dox2.relations)
    r1.extend(r2)
    return Doxament(r1)
