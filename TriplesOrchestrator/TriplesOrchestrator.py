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
    def traversVerbs(verbs):
        for verb in verbs:
            print "Main verb is", verb.baseverb.word
            Orchestrate.traverseRecursively(verb)
            Orchestrate.traverseVerbSibling(verb)

    @staticmethod
    def traverseRecursively(verb):
        if len(verb.children) == 0:
            return None
        elif len(verb.children) > 0:
            for child in verb.children:
                print "Child verb", child.baseverb.word
                Orchestrate.traverseRecursively(child)
                Orchestrate.traverseVerbSibling(child)

    @staticmethod
    def traverseVerbSibling(verb):
        if len(verb.verbsibling) == 0:
            return  None
        elif len(verb.verbsibling) > 0:
            for sibling in verb.children:
                print "sibling is", sibling.baseword.word
                Orchestrate.traverseVerbSibling(sibling)
                Orchestrate.traverseRecursively(sibling)

    @staticmethod
    def getTriples(G, target, root):
        tripleExtractor = extractor.TriplesExtractor.TriplesExtractor(G);

        triplesExtractorv2 = extractor.TriplesExtractorv2.TriplesExtractor(G, root);

        """
        for verb in triplesExtractorv2.construct_verbtree_structure():
            print "Verb is", verb.baseverb.word
            if verb.aux:
                print "AUX is", verb.aux.word
            if verb.auxpass:
                print "AUXPASS is", verb.auxpass.word
            if verb.advmod:
                print "ADVERB mod is", verb.advmod.word
            if verb.parent:
                print "parent is", verb.parent.baseverb.word
            if verb.vbz:
                print "VBZ is", verb.vbz.word
            if verb.jj:
                print "JJ is ", verb.jj.word
            for y in verb.verbsibling:
                print y
                print "sibling is", y

            for child in verb.children:
                if child.vbz:
                    print "VBZ is", child.vbz.word
                print "Children", child.baseverb.word
                if child.aux:
                    print "Aux verb", child.aux.word
                if child.auxpass:
                    print "Auxpass", child.auxpass.word
                if child.advmod:
                    print "ADVERB mod is", child.advmod.word
                if child.parent:
                    print "Parent is", child.parent.baseverb.word
                if child.jj:
                    print "JJ is", child.jj.word
                for x in child.children:
                    print "Children of child", child
                for y in child.verbsibling:
                    print "Sibling is", y.baseverb.word
                print "\n"
            print "\n"
        """
        verbs = triplesExtractorv2.construct_verbtree_structure()
        Orchestrate.traversVerbs(verbs);


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
