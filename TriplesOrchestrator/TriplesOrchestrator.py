import os
import nltk.data
import extractor
import networkx as nx
from ParseTreeConstructor.TreeConstructor import TreeConstructor
from parser.POSTreeParser import TreeParser
from extractor.TriplesExtractor import TriplesExtractor
from extractor.TriplesExtractorv2 import TriplesExtractor
from ParseTreeConstructor.TreeConstructor import TreeConstructor
from configuration.properties import OUTPUT_TRIPLES_DIR, INPUT_TEXT_DIR, TEMP_WORKING_DIR, DONE_DIR

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle');

class Orchestrate:

    @staticmethod
    def run():
        for _, _, files in  os.walk(INPUT_TEXT_DIR):
            for file in files:
                if not file.endswith('DS_Store'):
                    filePath=INPUT_TEXT_DIR+"/"+file
                    target = open(OUTPUT_TRIPLES_DIR+"/"+file, 'w')
                    print filePath
                    fp = open(filePath)
                    data = fp.read()
                    print data
                    for line in tokenizer.tokenize(data):
                        print line
                        tempFileOutput = TreeConstructor.callSyntaxNetShell(line, TEMP_WORKING_DIR)
                        root, G = TreeParser.get_parse_tree(tempFileOutput);
                        Orchestrate.getTriples(G, target, root)
                    target.close()

    @staticmethod
    def traversVerbs(verbs, triplesExtractor, target):
        for verb in verbs:
            verb = triplesExtractor.retrieve_subject(verb)
            verb = triplesExtractor.retrieve_objects(verb)
            target.write(verb.get_triple_format())
            target.write("\n")
            Orchestrate.traverseRecursively(verb, triplesExtractor, target)
            Orchestrate.traverseVerbSibling(verb, triplesExtractor, target)

    @staticmethod
    def traverseRecursively(verb, triplesExtractor, target):
        if len(verb.children) == 0:
            return None
        elif len(verb.children) > 0:
            for child in verb.children:
                child = triplesExtractor.retrieve_subject(child)
                child = triplesExtractor.retrieve_objects(child)
                target.write( child.get_triple_format())
                target.write("\n")
                Orchestrate.traverseRecursively(child, triplesExtractor, target)
                Orchestrate.traverseVerbSibling(child, triplesExtractor, target)

    @staticmethod
    def traverseVerbSibling(verb, triplesExtractor, target):
        if len(verb.verbsibling) == 0:
            return  None
        elif len(verb.verbsibling) > 0:
            for sibling in verb.children:
                sibling = triplesExtractor.retrieve_subject(sibling)
                sibling = triplesExtractor.retrieve_objects(sibling)
                target.write(sibling.get_triple_format())
                target.write("\n")
                Orchestrate.traverseVerbSibling(sibling, triplesExtractor)
                Orchestrate.traverseRecursively(sibling, triplesExtractor)



    @staticmethod
    def getTriples(G, target, root):
        triplesExtractorv2 = extractor.TriplesExtractorv2.TriplesExtractor(G, root);
        verbs = triplesExtractorv2.construct_verbtree_structure()
        Orchestrate.traversVerbs(verbs, triplesExtractorv2, target);

Orchestrate.run()
