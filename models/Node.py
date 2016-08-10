
class Node:
    """
    This class represents a node in the ParseTree object.

    A ParseTree is a K-ary tree constructed from a sentence.

    Each node have the following attributes
        word - word in the sentence
        POS - POS tag from the Parse Tree
        attribute - subj, obj etc
        children - List of children linked to this word in the parse tree.
        Each child will again be an object of class Node
    """

    def __init__(self, word, POS, attribute):
        """

        :param word:
        :param POS:
        :param attribute:
        :return:
        """
        self.word = word
        self.POS = POS
        self.attribute = attribute
        self.children = []

    def add_child(self, node):
        """

        :param node:
        :return:
        """
        self.children.append(node)
