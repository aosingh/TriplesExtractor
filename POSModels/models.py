class Node:
    def __init__(self):
        self.parent = None
        self.baseverb = None
        self.jj = None
        self.vbz = None;
        self.aux = None
        self.auxpass = None
        self.advmod = None
        self.objects = []
        self.subject = []
        self.children = []
        self.when = None
        self.where = None
        self.verbsibling = []

    def add_children(self, child):
        self.children.append(child)