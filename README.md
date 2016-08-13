# TriplesExtractor
TriplesExtractor is a Python package, which can be used to extract <Subject, Predicate, Object> triples from a document.

## Getting Started
These instructions will give you a copy of the project up and running on your local machine for development and testing purposes.

### Clone this Repo
Clone this repository into whatever directory you'd like to work on it from:

```bash
git clone https://github.com/aosingh/TriplesExtractor.git
```

### Install the following
*   [Python 2.7](https://www.python.org/download/releases/2.7/)
*   [Syntaxnet](https://github.com/tensorflow/models/tree/master/syntaxnet) 
*   [nltk](http://www.nltk.org/)  
*   [nltk.data](http://www.nltk.org/data.html)
*   [networkx](https://networkx.readthedocs.io/en/stable/download.html)

### Change the configuration
In file `TriplesExtractor/configuration/properties.py`, change the following

*  `SYNTAXNET_DIRECTORY` 
    * Path to your `models/syntaxnet` directory on your local system
*  `INPUT_TEXT_DIR`
    * Path to the location of your inputfiles
*  `TEMP_WORKING_DIR`
    * A temporary working location where the files will be kept while processing
*   `OUTPUT_TRIPLES_DIR`
    * Output directory where for each input file a corresponding output file with triples will be present after execution.
 
Below is an example of my `TriplesExtractor/configuration/properties.py`
```python
    SYNTAXNET_DIRECTORY="/home/abhishek/models/syntaxnet"
    INPUT_TEXT_DIR="/home/abhishek/PycharmProjects/TriplesExtractor/inputfiles"
    TEMP_WORKING_DIR="/home/abhishek/PycharmProjects/TriplesExtractor/workingdir"
    DONE_DIR="/Users/abhsingh/PycharmProjects/TripleExtractor/donedir"
    OUTPUT_TRIPLES_DIR="/home/abhishek/PycharmProjects/TriplesExtractor/output"
```



