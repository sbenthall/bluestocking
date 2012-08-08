bluestocking
============

An information extraction toolkit.

To discuss the project with use, join our maing list:
http://groups.google.com/forum/?fromgroups#!forum/bluestocking-dev

To run tests:

    python tests.py

To run factchecker demo:

    python factchecker.py "The sky is not blue."

This test a document against the simple English Wikipedia
articles for each word in the tested document.  Try
replacing test-factchecker.txt with your own text file!

(Warning: documents with long sentences take longer to query)

Scripts included:

### parse.py

Defines Document class for wrapping raw text and Parser
class for extracting Relations from a Document.

Relations encapsulate a semantically significant lexical
cooccurence.

Documents have a method to turn them into Doxaments (see below).

### doxament.py

Defines a Doxament class.  A Doxament contains many Relations.
A Doxament may be queried for consistency with another Doxament.  They may also be merged to form a more complete knowledge base.

### other

wikipedia.py and wiki2plain.py from 
http://stackoverflow.com/questions/4460921/extract-the-first-paragraph-from-a-wikipedia-article-python