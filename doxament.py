import parse
from pprint import pprint as pp

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
        contras = []
        
        for r in qdox:
            found += 1 if r in self else 0
            contra_rel = r.flip()
            if contra_rel in self:
                contras.append(contra_rel) 
                found -= 1

        score = float(found) / total
        return score, contras

    def add_relation(self,relation):
        d = self.relations.get(relation.item1,{})
        d[relation.item2] = relation.co
        self.relations[relation.item1] = d

    def __contains__(self,relation):
        try:
            co = self.relations[relation.item1][relation.item2]
            return co == relation.co
        except:
            return False

    def __iter__(self):
        for item1, item2_co in self.relations.items():
            for item2,co in item2_co.items():
                yield parse.Relation(co,item1,item2)

def merge(dox1, dox2):
    x1 = Doxament(dox1)
    for r in dox2:
        x1.add_relation(r)

    return x1

def compare_docs(doc1,doc2):
    dox1 = Doxament(doc1.parse_relations())
    dox2 = Doxament(doc2.parse_relations())

    return dox1.query(dox2)
