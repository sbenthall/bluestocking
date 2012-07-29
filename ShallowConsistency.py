from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.corpus import stopwords
from itertools import combinations
import itertools


def preprocess_doc(doc):
    sentence_tokenizer = PunktSentenceTokenizer()
    sentences = sentence_tokenizer.sentences_from_text(doc)    
    tokens = []
    for sentence in sentences:
        #sentence1 = sentence.split()
        sentence1 = neg_scope(sentence)
        tokens.extend(w for w in sentence1 if w.lower() not in stopwords.words("english"))
    for ii in xrange(len(tokens)):
        if tokens[ii][-1] == '.':
            tokens[ii] = tokens[ii][:-1]
    return tokens


def neg_scope(sentence):
    neg_words = ['not','never', 'isn\'t','was\'nt','hasn\'t']
    sentence = sentence.split()
    for ii in xrange(len(sentence)):
        if sentence[ii] in neg_words:
            for jj in range(ii+1,len(sentence)):
                sentence[jj] = 'neg_%s' % sentence[jj] 
    return sentence 


def shallow_sem_consist(doc1,doc2):
    summ_dox = preprocess_doc(doc1)
    check_dox = preprocess_doc(doc2)
    consist = 0
    inconsist = 0
    for word in check_dox:
        lemmas = list()
        if word[0:4] == "neg_":
            lemmas = aggregate_lemmas(word[4:],'antonym')
            for lem in lemmas:
                inconsist += 1 if lem in summ_dox else 0            
        else:
            lemmas = aggregate_lemmas(word,'synonym')
            for lem in lemmas:
                consist += 1 if lem in summ_dox else 0
    return (consist,inconsist)



