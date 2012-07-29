bluestocking
============

An information extraction toolkit.

To run tests:

   python tests.py


Scripts included:

parse.py
--------

Defines Document class for wrapping raw text and Parser
class for extracting Relations from a Document.

Relations encapsulate a semantically significant lexical
cooccurence.

Documents have a method to turn them into Doxaments (see below).

doxament.py
-----------

Defines a Doxament class.  A Doxament contains many Relations.
A Doxament may be queried for consistency with another Doxament.  They may also be merged to form a more complete knowledge base.


wikipedia.py and wiki2plain.py from 
http://stackoverflow.com/questions/4460921/extract-the-first-paragraph-from-a-wikipedia-article-python