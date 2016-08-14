import networkx as nx
from POSModels.models import Node


class TriplesExtractor:

    def __init__(self, G, root):
        self.G = G
        self.root = root
        self.seen_nodes = {}
        self.verbs =[]

    def set_aux_verbs(self, node, posnode):
        for child in self.G.successors(node):
            if(child.attribute == 'aux'):
                posnode.aux = child
            if(child.attribute == 'auxpass'):
                posnode.auxpass = child
            if(child.attribute == 'advmod'):
                posnode.advmod = child
        return posnode



    def get_verb_children(self, node, parentposnode):
        for child in self.G.successors(node):
            if child.POS in ('VBN', 'VB', 'VBD', 'VBG', 'VBP') \
                    and child.attribute not in ('aux', 'auxpass') \
                    and child != node:
                node5 = Node()
                node5.baseverb = child
                node5 = self.set_aux_verbs(child, node5)
                node5.parent = parentposnode

                if child in self.seen_nodes and self.seen_nodes[child] in self.verbs:
                    self.verbs.remove(self.seen_nodes[child])
                elif child not in self.seen_nodes:
                    self.seen_nodes[child] = node5
                node5 = self.check_for_conjunction(child, node5)
                parentposnode.add_children(node5)

            elif child.POS in ('VBZ') \
                    and child.attribute not in ('aux', 'auxpass') \
                    and child != node:
                node6 = Node()
                node6.vbz = child
                node6 = self.build_vbz_tree(child, node6)
                if child in self.seen_nodes and self.seen_nodes[child] in self.verbs:
                    self.verbs.remove(self.seen_nodes[child])
                elif child not in self.seen_nodes:
                    self.seen_nodes[child] = node6
                node6 = self.check_for_conjunction(child, node6)
                parentposnode.add_children(node6)
        return parentposnode

    def check_if_children(self, node):
        for child in self.G.successors(node):
            if(child.POS in (",")):
                return True
        return False

    def check_for_conjunction(self, node, posnode):
        for child in self.G.successors(node):
            if child.attribute in ('conj')\
                    and child.POS in ('VBN', 'VB', 'VBD', 'VBZ', 'VBG', 'VBP'):
                childNode = Node()
                childNode.baseverb = child

                if(self.check_if_children(child)):
                   childNode = self.get_verb_children(child, childNode)

                childNode = self.set_aux_verbs(child, childNode)
                posnode.verbsibling.append(childNode)

                if child in self.seen_nodes:
                    if self.seen_nodes[child] in self.verbs:
                        self.verbs.remove(self.seen_nodes[child])

                elif child not in self.seen_nodes:
                    self.seen_nodes[child] = childNode

                if posnode.parent \
                        and posnode.parent != posnode:
                    childNode.parent = posnode.parent
                    posnode.parent.add_children(childNode)
        return posnode


    def build_vbz_tree(self, node, posnode):
        if node.attribute in ('cop', 'aux', 'auxpass'):
            parent  = self.G.predecessors(node)[0]
            if parent.POS in ('JJ', 'NN'):
                posnode.jj = parent
                for child in self.G.successors(parent):
                    if child.POS in ('VBN', 'VB', 'VBD', 'VBG', 'VBP'):
                        if child in self.seen_nodes:
                            if self.seen_nodes[child] in self.verbs and self.seen_nodes[child] in self.verbs:
                                self.verbs.remove(self.seen_nodes[child])

                        elif child not in self.seen_nodes:
                            self.seen_nodes[child] = posnode

                        posnode = self.set_aux_verbs(child, posnode)
                        if self.check_if_children(child):
                            posnode = self.get_verb_children(child, posnode)
                        posnode = self.check_for_conjunction(child, posnode)
                        posnode.baseverb = child
                    elif child.attribute in ('advmod'):
                        posnode.advmod = child
            elif parent.POS in ('VBN', 'VB', 'VBD', 'VBG', 'VBP'):
                    if parent in self.seen_nodes:
                        if self.seen_nodes[parent] in self.verbs:
                            self.verbs.remove(self.seen_nodes[parent])
                    elif parent not in self.seen_nodes:
                        self.seen_nodes[parent] = posnode
                    posnode = self.set_aux_verbs(parent, posnode)
                    if self.check_if_children(parent):
                        posnode = self.get_verb_children(parent, posnode)
                    posnode = self.check_for_conjunction(parent, posnode)
                    posnode.baseverb = parent
        elif node.attribute in ('advcl', 'ccomp'):
            for child in self.G.successors(node):
                if child.POS in ('VBN', 'VB', 'VBD', 'VBG', 'VBP'):

                    if child in self.seen_nodes:
                        if self.seen_nodes[child] in self.verbs:
                            self.verbs.remove(self.seen_nodes[child])

                    elif child not in self.seen_nodes:
                        self.seen_nodes[child] = posnode


                    posnode = self.set_aux_verbs(child, posnode)
                    if(self.check_if_children(child)):
                        posnode = self.get_verb_children(child, posnode)
                    posnode = self.check_for_conjunction(child, posnode)
                    posnode.baseverb = child
        if not posnode.baseverb:
                posnode.baseverb = posnode.vbz
                posnode.vbz = None
                posnode = self.set_aux_verbs(node, posnode)
                if(self.check_if_children(node)):
                    posnode = self.get_verb_children(node, posnode)
                posnode = self.check_for_conjunction(node, posnode)
        return posnode


    def construct_verbtree_structure(self):
        for node in self.G.node:

            if node.POS in ('VBN', 'VB', 'VBD', 'VBG', 'VBP') \
                    and node not in self.seen_nodes \
                    and node.attribute not in ('aux', 'auxpass'):
                node4 = Node()
                node4.baseverb = node
                node4 = self.set_aux_verbs(node, node4)
                self.verbs.append(node4)
                self.seen_nodes[node] = node4
                if(self.check_if_children(node)):
                    node4 = self.get_verb_children(node, node4)
                node4 = self.check_for_conjunction(node, node4)


            elif node.POS in ('VBZ') \
                    and node not in self.seen_nodes:
                node5 = Node()
                node5.vbz = node
                self.verbs.append(node5)
                self.seen_nodes[node] = node5
                node5 = self.build_vbz_tree(node, node5)
        return self.verbs


    def retrieve_subject(self, verbnode):
        for child in self.G.successors(verbnode.baseverb):
            if child.attribute in ('nsubj', 'nsubjpass'):
                verbnode.subject.append(child)
        for child in self.G.predecessors(verbnode.baseverb):
            if child.attribute in ('nsubj', 'nsubjpass'):
                verbnode.subject.append(child)

        if(verbnode.jj):
            for child in self.G.successors(verbnode.jj):
                if child.attribute in ('nsubj'):
                    verbnode.subject.append(child)

        if len(verbnode.subject) == 0:
            parent = self.G.predecessors(verbnode.baseverb)[0]
            while parent.POS not in ('NN', 'NNS') and (parent.attribute != 'ROOT'):
                print parent.word
                print parent.attribute
                parent = self.G.predecessors(parent)[0]
            verbnode.subject.append(parent)
        return verbnode


    def retrieve_objects(self, verbnode):
        for child in self.G.successors(verbnode.baseverb):
            if child.attribute in ('pobj', 'dobj'):
                self.retrieve_children_of_noun(child, verbnode.objects)
                verbnode.objects.append(child)

            if child.attribute in ('prep'):
                verbnode.objects.append(child)
                verbnode = self.retrieveObjectsFromPrep(verbnode, child)
        if(verbnode.jj):
            for edges in list(nx.bfs_edges(self.G, verbnode.jj)):
                if edges[1].attribute == 'prep':
                    verbnode  = self.retrieveObjectsFromPrep(verbnode, edges[1])
        return verbnode


    def retrieveObjectsFromPrep(self, verbnode, prepnode):
        for child in self.G.successors(prepnode):
            if child.attribute in ('pobj') and child.POS in ('NN'):
                verbnode.where = child
            elif child.attribute in ('pobj', 'dobj'):
                verbnode.objects.append(child)

        return verbnode


    def retrieve_children_of_noun(self, nounnode, objects):
        for edges in list(nx.bfs_edges(self.G, nounnode)):
            if (edges[1].attribute in ('num')):
                objects.append(edges[1])
        return objects














