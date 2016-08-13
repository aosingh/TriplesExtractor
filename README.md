# TriplesExtractor
TriplesExtractor is a Python package, which can be used to extract `<Subject, Predicate, Object>` triples from a document.

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
    * python 2.7:
    * python 3 support is not available yet
    *   bazel:
        *   **versions 0.2.0 - 0.2.2b, NOT 0.2.3**
        *   follow the instructions [here](http://bazel.io/docs/install.html)
    *   swig:
        *   `apt-get install swig` on Ubuntu
        *   `brew install swig` on OSX
    *   protocol buffers, with a version supported by TensorFlow:
    *   check your protobuf version with `pip freeze | grep protobuf`
    *   upgrade to a supported version with `pip install -U protobuf==3.0.0b2`
    *   asciitree, to draw parse trees on the console for the demo:
        *   `pip install asciitree`
    *   numpy, package for scientific computing:
        *   `pip install numpy`
Once you completed the above steps, you can build and test SyntaxNet with the
following commands:

```shell
  git clone --recursive https://github.com/tensorflow/models.git
  cd models/syntaxnet/tensorflow
  ./configure
  cd ..
  bazel test syntaxnet/... util/utf8/...
  # On Mac, run the following:
  bazel test --linkopt=-headerpad_max_install_names \
    syntaxnet/... util/utf8/...
```

Bazel should complete reporting all tests passed.

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

## Development
Run the following python class to test if everything is correctly set.
You can place a test input file at the `INPUT_TEXT_DIR` location.
if the program runs successfully and exits with 0, you will find the corresponding output file at `OUTPUT_TRIPLES_DIR`
```bash
python TriplesExtractor/TriplesOrchestrator/TriplesOrchestrator.py

``` 

