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
    def traversVerbs(verbs, triplesExtractor):
        for verb in verbs:
            print "Main verb is", verb.baseverb.word
            if(verb.aux):
                print "Aux is", verb.aux.word
            if(verb.vbz):
                print "VBZ is", verb.vbz.word
            if(verb.auxpass):
                print "AUXPASS is", verb.auxpass.word
            if(verb.advmod):
                print "ADVERB MOD is", verb.advmod.word
            if(verb.jj):
                print "JJ or NN is", verb.jj.word
            verb = triplesExtractor.retrieve_subject(verb)
            verb = triplesExtractor.retrieve_objects(verb)
            for x in verb.subject:
                print "Subject is", x.word
            for y in verb.objects:
                print "OBJECTS are", y.word
            print "\n"
            Orchestrate.traverseRecursively(verb, triplesExtractor)
            Orchestrate.traverseVerbSibling(verb, triplesExtractor)

    @staticmethod
    def traverseRecursively(verb, triplesExtractor):
        if len(verb.children) == 0:
            return None
        elif len(verb.children) > 0:
            for child in verb.children:
                print "Child verb", child.baseverb.word
                if(child.aux):
                    print "Aux is", child.aux.word
                if(child.vbz):
                    print "VBZ is", child.vbz.word
                if(child.auxpass):
                    print "AUXPASS is", child.auxpass.word
                if(child.advmod):
                    print "ADVERB MOD is", child.advmod.word
                if(child.jj):
                    print "JJ or NN is", child.jj.word
                child = triplesExtractor.retrieve_subject(child)
                child = triplesExtractor.retrieve_objects(child)
                for x in child.subject:
                    print "Subject is", x.word
                for y in child.objects:
                    print "OBJECTS are", y.word
                print "\n"
                Orchestrate.traverseRecursively(child, triplesExtractor)
                Orchestrate.traverseVerbSibling(child, triplesExtractor)

    @staticmethod
    def traverseVerbSibling(verb, triplesExtractor):
        if len(verb.verbsibling) == 0:
            return  None
        elif len(verb.verbsibling) > 0:
            for sibling in verb.children:
                print "sibling is", sibling.baseword.word
                sibling = triplesExtractor.retrieve_subject(sibling)
                sibling = triplesExtractor.retrieve_objects(sibling)
                for x in sibling.subject:
                     print "Subject is", x.word
                for y in sibling.objects:
                    print "OBJECTS are", y.word
                print "\n"
                Orchestrate.traverseVerbSibling(sibling, triplesExtractor)
                Orchestrate.traverseRecursively(sibling, triplesExtractor)



    @staticmethod
    def getTriples(G, target, root):
        tripleExtractor = extractor.TriplesExtractor.TriplesExtractor(G);
        triplesExtractorv2 = extractor.TriplesExtractorv2.TriplesExtractor(G, root);
        verbs = triplesExtractorv2.construct_verbtree_structure()
        Orchestrate.traversVerbs(verbs, triplesExtractorv2);


        for verb in tripleExtractor.getVerbs():
            subjects, objects, newverb = tripleExtractor.getSubjectsAndObjectsForVerb(verb)

            for object in objects:
                for obj in objects:
                    if object in obj and object != obj:
                        print object
#                        objects.remove(object)

            for object in subjects:
                for obj in subjects:
                    if object in obj and object != obj:
                        print object
                        subjects.remove(object)

            subjects.reverse();
            subj = "";
            print subj

            for subject in subjects:
                subj = subj +" "+subject

            if len(objects) == 0:
                target.write("("+subj+", "+verb.word+", "+" "+")")
                target.write("\n")

            for obj in objects:
               target.write("("+ subj+", "+verb.word+", "+obj+")")
               target.write("\n")

Orchestrate.run()
