import doxament

from itertools import combinations
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.corpus import stopwords
            
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
        return doxament.Doxament(Parser(self).parse_relations())

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
        sentences = self.preprocess(sentences)

        relations = []
        for sentence in sentences:            
            relations.extend(self.parse_sentence(sentence))

        return relations

    def preprocess(self, sentences):
        '''
        Takes a list of strings representing sentences.
        Returns list of processed tokens, suitable for
        converting to Relations.
        '''
        post = []

        for sentence in sentences:
            # part of speech
            # chunking
            # pronoun resolution
            ps = self.neg_scope(sentence)
            ps = [w for w in ps if w.lower() not in stopwords.words("english")]
            post.append(ps)

        return post

    def neg_scope(self, sentence):
        neg_words = ['not','never', 'isn\'t','was\'nt','hasn\'t']
        for ii in xrange(len(sentence)):
            if sentence[ii] in neg_words:
            #should really go to next punctuation pt, complementizer(?), clause-boundary 
                for jj in range(ii+1,len(sentence)):
                    sentence[jj] = 'neg_%s' % sentence[jj]
        
        return sentence

    def parse_sentence(self,sentence):
            pairs = combinations(sentence,2)
            relations = [self.make_relation(p) for p in pairs]
            return relations

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
            return word[4:]
        else:
            return word

    def is_neg(self,word):
        return word[0:4] == "neg_"


