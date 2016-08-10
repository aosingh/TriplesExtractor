import networkx as nx



class TriplesExtractor:

    def __init__(self, G):
        self.G = G

    def getVerbs(self):
        verbs = []
        for x in self.G.node:
            if str(x.POS) in ('VBN', 'VB', 'VBD', 'VBZ', 'VBG', 'VBP'):
                verbs.append(x)
        return verbs


    def getNounsRecursive(self, node):
        noun = node.word;
        for child in self.G.successors(node):
            if child.POS in ('JJ', 'VBG', 'CD', 'DT'):
                noun = child.word +" "+noun
        return noun


    def getNouns(self, node):
        nouns = []
        adjectives = []
        for edges in list(nx.bfs_edges(self.G, node)):
            if edges[1].POS in ('VBN', 'VB', 'VBD', 'VBZ', 'VBG', 'VBP'):
                return nouns
            if edges[1].POS in ('NN', 'NNP', 'NNPS', 'NNS', 'JJ', 'DT'):
                if edges[0].word in nouns:
                   nouns.remove(edges[0].word)
                if edges[0].POS in ('IN'):
                    word =  edges[0].word+" "+self.getNounsRecursive(edges[1])
                else:
                    word = self.getNounsRecursive(edges[1])+" "+edges[0].word
                nouns.append(word)
        return nouns

    def getNounsForSubjects(self, node):
        nouns = []
        for edges in list(nx.bfs_edges(self.G, node)):
            if edges[1].POS in ('VBN', 'VB', 'VBD', 'VBZ', 'VBG', 'VBP'):
                return nouns
            if edges[1].POS in ('NN', 'NNP', 'NNPS', 'NNS', 'JJ'):
                if edges[0].word in nouns:
                   nouns.remove(edges[0].word)
                word =  self.getNounsRecursive(edges[1])
                nouns.append(word)
        return nouns


    def getSubjectsAndObjectsForVerb(self, verb):
        subjects = []
        objects = []
        newverb = verb.word
        subject_object_map = []
        if verb.attribute == 'ROOT':
            for child in self.G.successors(verb):
                if  child.attribute in ('nsubj', 'nsubjpass'):
                    subjects.append(child.word)
                    subjects = subjects + self.getNounsForSubjects(child)
                elif child.POS in ('NN', 'NNP', 'NNPS', 'NNS', 'JJ'):
                    objects.append(child.word)
                elif child.POS == 'IN':
                    objects = objects + self.getNouns(child)
        else:
             for child in self.G.successors(verb):
                if child.POS not in ('VBN', 'VB', 'VBD', 'VBZ', 'VBG', 'VBP'):
                    if child.attribute in ('nsubj', 'nsubjpass'):
                        subjects.append(child.word)
                        subjects = subjects + self.getNounsForSubjects(child)
                    elif child.POS in ('NN', 'NNP', 'NNPS', 'NNS', 'JJ'):
                        objects.append(child.word)
                        objects = objects + self.getNouns(child)
                    elif child.POS == 'IN':
                        objects = objects + self.getNouns(child)

             parent = self.G.predecessors(verb)[0]
             while parent.POS not in ('NN', 'NNP', 'NNPS', 'NNS'):
                parent = self.G.predecessors(parent)[0]
                if parent.attribute == 'ROOT':
                    return subjects, objects, newverb

             for child in self.G.successors(parent):
                     if child.attribute == 'nsubj' and child.POS != 'PRP':
                         newverb = verb.word +" "+parent.word
                         subjects.append(child.word)
                         subjects = subjects + self.getNounsForSubjects(child)
                     elif child.POS == 'PRP':
                         subjects.append(child.word)
                         subjects = subjects + self.getNounsForSubjects(child)
                         objects.append(parent.word)
                     elif parent.POS in ('NN', 'NNP', 'NNPS', 'NNS', 'JJ') and parent.attribute != "ROOT":
                         if parent.word not in subjects:
                            subjects.append(parent.word)
                            subjects = subjects + self.getNounsForSubjects(parent)
                     elif child.POS == 'IN':
                        objects = objects + self.getNouns(child)

        return subjects, objects, newverb

