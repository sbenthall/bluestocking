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
        return doxament.Doxament(Parser(self).parse_relations())    

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
        sentence_tokenizer = PunktSentenceTokenizer()
        sentences = sentence_tokenizer.sentences_from_text(self.doc.text)
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
            ps = [word.strip(",.?!") for word in ps]
            ps = [w for w in ps if w.lower() not in stopwords.words("english")]
            post.append(ps)

        return post

    def neg_scope(self, sentence):
        neg_words = ['not','never', 'isn\'t','was\'nt','hasn\'t']
        sentence = sentence.split()
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

        return Relation(co,item1,item2)

    def strip_neg(self,word):
        if word[0:4] == "neg_":
            return word[4:]
        else:
            return word

    def is_neg(self,word):
        return word[0:4] == "neg_"


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
            if self.co == other.co:
                return ((syno(self.item1,other.item1) and
                         syno(self.item2,other.item2)) or
                        (anto(self.item1,other.item1) and
                         anto(self.item2,other.item2)))
            else:
                return ((syno(self.item1,other.item1) and
                         anto(self.item2,other.item2)) or
                        (anto(self.item1,other.item1) and
                         syno(self.item2,other.item2)))
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str((self.co, self.item1, self.item2))

    def __repr__(self):
        return str((self.co, self.item1, self.item2))



def syno(item1,item2):
    #should test synsets, this is dummy
    return item1 == item2

def anto(item1,item2):
    #should test antonyms, this is dummy
    return False

def aggregate_lemmas(word,relation):
    '''
    Generates a list of synonyms/antonyms for :word: 
    '''
    lems = set()
    if relation == "synonym":
        sets = [syn.lemmas for syn in wn.synsets(word)]
    elif relation == "antonym":
        sets = [syn.lemmas for syn in wn.synsets(word)]
        sets = list(itertools.chain(*sets))
        sets = [x.antonyms() for x in sets]
        sets = [x for x in sets if x]
        
    sets = list(itertools.chain(*sets))
    sets = [lem.name for lem in sets]
    for x in sets:
        lems.add(x)
    return lems

