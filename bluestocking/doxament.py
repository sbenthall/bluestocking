import parse
from pprint import pprint as pp
from nltk.corpus import wordnet as wn
from itertools import chain

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


class Relation:
    co = True
    item1 = ''
    item2 = ''

    def __init__(self,co,item1,item2):
        self.co = co
        self.item1 = item1.lower()
        self.item2 = item2.lower()

    def flip(self):
        return Relation(not self.co, self.item1, self.item2)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.co == other.co:
                # currently, relations represent
                # cooccurence not predication
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
    return item1 in aggregate_lemmas(item2,'synonym')

def anto(item1,item2):
    return item1 in aggregate_lemmas(item2,'antonym')

def aggregate_lemmas(word,relation):
    '''
    Generates a list of synonyms/antonyms for :word:
    '''
    lems = set()
    if relation == "synonym":
        sets = [syn.lemmas for syn in wn.synsets(word)]
    elif relation == "antonym":
        sets = [syn.lemmas for syn in wn.synsets(word)]
        sets = list(chain(*sets))
        sets = [x.antonyms() for x in sets]
        sets = [x for x in sets if x]

    sets = list(chain(*sets))
    sets = [lem.name for lem in sets]
    for x in sets:
        lems.add(x)
    return lems
