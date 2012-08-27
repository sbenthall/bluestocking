import nltk
import chunkerator
import doxament 

from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from itertools import combinations
 

class Document:
    '''
    A class that represents unprocessed text.
    May later include metadata.
    '''

    text = ''

    def __init__(self,text):
        self.text = text
        
    def __str__(self):
        return self.text

    def to_dox(self):
        return Doxament(Parser(self).parse_relations())

    def tokenize(self):
        '''
        Returns a list of tokenized sentences
        '''
        sentence_tokenizer = PunktSentenceTokenizer()
        sentences = sentence_tokenizer.sentences_from_text(self.text)
        sentences = [sentence.split() for sentence in sentences]
        sentences = [[word.strip(",.?!") for word in sentence]
                     for sentence in sentences]
        return sentences

class Parser:
    '''
    Class responsible for parsing a Document into
    a collection of Relations.
    '''
    doc = ''

    # initialize with a Document
    def __init__(self, doc):
        self.doc = doc

    def parse_relations(self):
        sentences = self.doc.tokenize()
        sentences,chunker = self.preprocess(sentences)

        relations = []
        for sentence in sentences:            
            relations.extend(self.parse_sentence(sentence,chunker))

        return relations

    def preprocess(self, sentences):
        '''
        Takes a list of strings representing sentences.
        Returns list of processed tokens, suitable for
        converting to Relations.
        '''
        rules = """
		    NP: {<DT>?<JJ>*<NN.*>}
		    NP: {<PRP>}
		"""
        post = []
        c = chunkerator.Chunkerator(rules,True)
        for sentence in sentences:
            sent = c.chunk_sent(sentence)
            ps = [w for w in sent if w.lower() not in stopwords.words("english")]
            post.append(ps)

        return post, c

    def parse_sentence(self,sentence,chunkerator):
            relations = []
            # adding noun chunk internal relations
            for chunk in chunkerator.chunksSeen:
                g = doxament.Relation(True,chunk,chunkerator.chunksSeen[chunk])
                relations.append(g)
                splitchunkpairs = combinations(chunk.split('_'),2)
                chunkRels = [self.make_relation(x) for x in splitchunkpairs]
                relations.extend(chunkRels)
            # adding sentence relations 
            pairs = combinations(sentence,2)
            sentRels = [self.make_relation(p) for p in pairs]
            relations.extend(sentRels)
            self.remove_negwords(relations)
            return relations
    
    def remove_negwords(self,relations):
        '''
        Removes any relation from doxament whose key is a neg_word
        '''
        neg_words = ['not','never', 'isn\'t','was\'nt','hasn\'t','haven\'t',"didn't",'don\'t','doesn\'t']
        for word in neg_words:
            if word in relations:
                del relations[word]
                
    def make_relation(self,pair):
        co = True
        item1,item2 = pair

        if self.is_neg(item1):
            item1 = self.strip_neg(item1)
            co = not co

        if self.is_neg(item2):
            item2 = self.strip_neg(item2)
            co = not co

        return doxament.Relation(co,item1,item2)

    def strip_neg(self,word):
        if word[0:4] == "neg_":
            return word.lstrip('neg_')
        else:
            return word

    def is_neg(self,word):
        return word[0:4] == "neg_"


senttt2 = 'The man didn\'t make some green engines, and The woman did yoga.'
text1 = "Today was a good day.  Yesterday was a bad day."
doc1 = Document(senttt2)
dox1 = doc1.to_dox()
print dox1.relations
