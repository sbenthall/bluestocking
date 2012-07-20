import parse

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
            contra_rel = r.flip()
            if contra_rel in self.relations:
                contras.append(contra_rel) 
                found -= 1

        score = float(found) / total
        return score, contras

def merge(dox1, dox2):
    r1 = list(dox1.relations)
    r2 = list(dox2.relations)
    r1.extend(r2)
    return Doxament(r1)

def compare_docs(doc1,doc2):
    dox1 = Doxament(doc1.parse_relations())
    dox2 = Doxament(doc2.parse_relations())

    return dox1.query(dox2)
