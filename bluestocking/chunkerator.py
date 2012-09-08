import nltk
import types
from nltk import tag, chunk

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

    def neg(self, tree):
        neg_words = ['not','never', 'isn\'t','was\'nt','hasn\'t','haven\'t','didn\'t','don\'t','doesn\'t']
        for ii in xrange(len(tree)):
            if tree[ii][0] in neg_words:
                for jj in range(ii+1,len(tree)):
                    if type(tree[jj][0]) != types.TupleType:
                        if tree[jj][1][1]!="C":
                            blob = 'neg_%s' % str(tree[jj][0])
                            tree[jj] = (blob,tree[jj][1])
                        else:
                            break
        return tree
    
    
    def remake_chunked_sent(self,tree):
        '''
        Reconstitutes the original sentence with chunks treated as atomic.
        '''
        output = '' 
        neg_words = ['not','never', 'isn\'t','was\'nt','hasn\'t','haven\'t','didn\'t','don\'t','doesn\'t']
        for xx in tree:
            if type(xx[0]) == types.TupleType:      
                output+= str(self.merge_chunk(xx))+' '
            elif xx[0] not in neg_words:
                output+= str(xx[0])+' '
        output.rstrip()
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
        tree = self.neg(tree)
        out_sent = self.remake_chunked_sent(tree)
        if self.nounChunking:
            out_sent = self.replace_chunk_with_head(out_sent)
        return out_sent
