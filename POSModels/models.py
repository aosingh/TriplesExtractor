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
        self.prep = None

    def add_children(self, child):
        self.children.append(child)

    def get_triple_format(self):
        tripleString = "(";
        if(self.subject):
            for subj in reversed(self.subject):
                tripleString = tripleString+subj.word+" "
        tripleString = tripleString+", "
        tripleString  = tripleString + self.get_the_verb()
        tripleString = tripleString + ", "
        if(self.objects):
            for obj in self.objects:
                tripleString = tripleString+obj.word+" "
        if(self.when):
            tripleString = tripleString +"["+ self.when+"]"
            tripleString = tripleString + ", "
        if(self.where):
            tripleString = tripleString + "["+ self.where+"]"
        return tripleString +")"

    def get_the_verb(self):
        """

        :return:
        """
        verb = ""
        if(self.aux):
            verb = verb+self.aux.word+" "
        if(self.auxpass):
            verb = verb+self.auxpass.word+" "
        if(self.vbz):
            if(self.aux is None):
                verb = verb + self.vbz.word + " "
            elif(self.vbz.word != self.aux.word):
                verb = verb + self.vbz.word + " "
        if(self.baseverb):
            verb = verb+self.baseverb.word+" "
        if(self.jj):
            verb = verb+self.jj.word+" "
        if (self.prep):
            verb = verb+self.prep.word
        return verb




