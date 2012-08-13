
import nltk
import types
from nltk import tag, chunk
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from itertools import combinations

rules = """
    NP: {<DT>?<JJ>*<NN.*>}
    NP: {<PRP>}
"""

clauseRules = """
            CP: {<PRP> <VB.*>*<VB.*>+ <N+.*>} 
            CP: {<N+.*> <VB.*>*<VB.*>+ <N+.*>} 
            """
 
class Doxament:
    relations = {}

    def __init__(self, relations):
        '''
        Note argument can be either a list
        of relations or another Doxament.
        '''
        self.relations = {}
        for relation in relations:
            self.add_relation(relation)

    def query(self, qdox):
        '''
        Query the first doxament with the second
        doxament for consistency/coverage
        '''
        total = len(qdox.relations)
        found = 0
        supported = []
        contras = []
        novel = []

        for r in qdox:
            if r in self:
                found += 1
                supported.append(r)
            elif r.flip() in self:
                found -= 1
                contras.append(r)
            else:
                novel.append(r)

        score = float(found) / total
        return score, contras, supported, novel

    def add_relation(self,relation):
        d = self.relations.get(relation.item1,{})
        d[relation.item2] = relation.co
        self.relations[relation.item1] = d

    def __contains__(self,relation):
        # attempting to maintain the same equality standards
        # as in the Relation's class equality function
        # is awkward.  Would it be better for Relation
        # equality to be simpler? or be a facet of
        # Doxament implementation?
        syn1 = aggregate_lemmas(relation.item1,'synonym')
        anto1 = aggregate_lemmas(relation.item1,'antonym')
        syn2 = aggregate_lemmas(relation.item2,'synonym')
        anto2 = aggregate_lemmas(relation.item2,'antonym')

        syn_preds = {}
        for s1 in syn1:
            try:
                # adds any synonymous relations
                syn_preds.update(self.relations[s1])
            except:
                pass

        anto_preds = {}
        for a1 in anto1:
            try:
                anto_preds.update(self.relations[a1])
            except:
                pass

        for i2,co in syn_preds.items():
            if i2 in syn2 and co == relation.co:
                return True
            elif i2 in anto2 and co != relation.co:
                return True

        for i2,co in anto_preds.items():
            if i2 in anto2 and co == relation.co:
                return True
            elif i2 in syn2 and co == relation.co:
                return True

        return False

    def __iter__(self):
        for item1, item2_co in self.relations.items():
            for item2,co in item2_co.items():
                yield Relation(co,item1,item2)

def merge(dox1, dox2):
    x1 = Doxament(dox1)
    for r in dox2:
        x1.add_relation(r)

    return x1

def compare_docs(doc1,doc2):
    dox1 = Doxament(doc1.parse_relations())
    dox2 = Doxament(doc2.parse_relations())

    return dox1.query(dox2)
 

         
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
        post = []
        c = Chunkerator(rules,True)
        clauses = ClauseChunkerator(c)
        for sentence in sentences:
            # part of speech
            sent = c.chunk_sent(sentence)
            sent = clauses.chunk_sent(sent)
            # pronoun resolution
            print sent
            ps = self.neg_scope(sent)
            ps = [w for w in ps if w.lower() not in stopwords.words("english")]
            post.append(ps)

        return post,[c,clauses]

    def neg_scope(self, sentence):
        neg_words = ['not','never', 'isn\'t','was\'nt','hasn\'t']
        for ii in xrange(len(sentence)):
            if sentence[ii] in neg_words:
            #should really go to next punctuation pt, complementizer(?), clause-boundary 
                for jj in range(ii+1,len(sentence)):
                    sentence[jj] = 'neg_%s' % sentence[jj]
        
        return sentence

    def parse_sentence(self,sentence,chunkerators):
            relations = []
            for chunker in chunkerators:
                if chunker.nounChunking:
                    for chunk in chunker.chunksSeen:
                        g = Relation(True,chunk,chunker.chunksSeen[chunk])
                        relations.append(g)
                        splitchunkpairs = combinations(chunk.split('_'),2)
                        chunkRels = [self.make_relation(x) for x in splitchunkpairs]
                        relations.extend(chunkRels)
                else:
                    for chunk in chunker.chunksSeen:
                        splitchunkpairs = combinations(chunk.split('_'),2)
                        chunkRels = [self.make_relation(x) for x in splitchunkpairs]
                        relations.extend(chunkRels)
        
            #pairs = combinations(sentence,2)
            #relations = [self.make_relation(p) for p in pairs]
            #for chunk in chunkerator.chunksSeen:
            #    g = Relation(True,chunk,chunkerator.chunksSeen[chunk])
            #    relations.append(g)
            #    splitchunkpairs = combinations(chunk.split('_'),2)
            #    chunkRels = [self.make_relation(x) for x in splitchunkpairs]
            #    relations.extend(chunkRels)
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
            return word.lstrip('neg_')
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


class Chunkerator:

    def __init__(self, rules, nounChunking):
        self.chunkParser = nltk.RegexpParser(rules)
        self.chunksSeen = dict()
        self.nounChunking = nounChunking

    def initial_tag(self,sentence):
        '''
        Uses the basic nltk tagger to assign tags.
        '''
        #sent = sentence.split()
        print tag.pos_tag(sentence)
        return tag.pos_tag(sentence)

    def initial_chunk(self,tagged_sent):
        tree =  self.chunkParser.parse(tagged_sent)
        return tree

    def merge_chunk(self,tup):
        '''
        Reads in tuple from tree, flattens it out as atomic word.
        Finds head noun of every chunk.
        '''
        out = ''
        headNoun = str()
        for phrase in tup:
            #flatten out the chunk, conjoun with '_'
            out+=(str(phrase[0])+str('_'))
            #if tag of word is any kind of noun, treat as head 
            if self.nounChunking and (phrase[1][1] == "N" or phrase[1] == "PRP"):
                headNoun = phrase[0]    
        out = out.rstrip('_')
        if self.nounChunking:
            self.chunksSeen[out] = headNoun
        return out

    def remake_chunked_sent(self,tree):
        '''
        Reconstitutes the original sentence with chunks treated as atomic.
        '''
        output = '' 
        for xx in tree:
            if type(xx[0]) == types.TupleType:      
                output+= str(self.merge_chunk(xx))+' '
            else:
                output+= str(xx[0])+' '
        output.rstrip()
        print output
        return output.split()

    def replace_chunk_with_head(self, sentence):
        for x in xrange(0,len(sentence)):
            if sentence[x] in self.chunksSeen:
                sentence[x] = self.chunksSeen[sentence[x]]
        return sentence

    def chunk_sent(self,sentence):
        '''
        Chunks a sentence (into nouns or clauses, based on init rules)
        If chunking by noun, will replace noun chunks with new entity IDs.
        '''
        tagged_sent = self.initial_tag(sentence)
        tree = self.initial_chunk(tagged_sent)
        out_sent = self.remake_chunked_sent(tree)
        if self.nounChunking:
            out_sent = self.replace_chunk_with_head(out_sent)
        return out_sent



class ClauseChunkerator(Chunkerator):
    
    def __init__(self,Chunker):
        self.nounChunker = Chunker
        self.chunkParser = nltk.RegexpParser(clauseRules)
        self.chunksSeen = dict()
        self.nounChunking = False
        
    def initial_tag(self, sentence):
        return self.nounChunker.initial_tag(sentence)


    def chunk_sent(self,sentence):
        tagged_sent = self.initial_tag(sentence)
        tree = self.initial_chunk(tagged_sent)
        out_sent = self.remake_chunked_sent(tree)
        for chunk in out_sent:
            self.chunksSeen[chunk] = chunk
        return out_sent




                
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

senttt2 = 'The man made some green engines and The woman did yoga.'
text1 = "Today was a good day.  Yesterday was a bad day."
doc1 = Document(senttt2)
dox1 = doc1.to_dox()
print dox1.relations
