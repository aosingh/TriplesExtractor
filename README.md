# TriplesExtractor
===================
TriplesExtractor is a Python package, which can be used to extract <Subject, Predicate, Object> triples from a document.

## Getting Started
These instructions will give you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequesites
The following packages are needed to run TriplesExtractor
    
    *   [Python 2.7](https://www.python.org/download/releases/2.7/)
    *   [Syntaxnet](https://github.com/tensorflow/models/tree/master/syntaxnet) - This is needed to get the Parts-of-Speech(POS)
        tagging. Installing syntaxnet might take a while. Please read the instructions carefully.
    *   [nltk](http://www.nltk.org/) - Tokenizer i.e. extracting sentences from a paragraph.
    *   [networkx](https://networkx.readthedocs.io/en/stable/download.html) - A python package for the Graph datastructure 