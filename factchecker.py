import doxament
import parse
import sys
import wikipedia
import wiki2plain

from itertools import chain
from nltk.corpus import stopwords


lang = 'simple'
wiki = wikipedia.Wikipedia(lang)

def lookup_word(word):
    dox = doxament.Doxament([])

    try:
        print 'Looking up %s' % (word)
        raw = wiki.article(word)
    except:
        print 'Lookup failed'
        raw = None

    if raw:
        w2p = wiki2plain.Wiki2Plain(raw)
        content = w2p.text
        dox = parse.Document(content).to_dox()

    return dox

def main():
    text = "Uruguay is not in South America."

    try:
        text = sys.argv[1]
    except:
        print 'No text provided, using default'
        
    doc = parse.Document(text)
    sentences = doc.tokenize()
    
    words = set([w for sentence in sentences for w in sentence if w.lower() not in stopwords.words("english")])

    doxes = [lookup_word(w) for w in words]

    print 'Building knowledge base'
    kb = reduce(doxament.merge,doxes)

    print 'Querying knowledge base with original document'
    print kb.query(doc.to_dox())

if __name__ == '__main__':
    main()
