import re
import os
import networkx as nx
from models.Node import Node
from ParseTreeConstructor.TreeConstructor import TreeConstructor
from extractor.TriplesExtractor import TriplesExtractor


class TreeParser:

    @staticmethod
    def get_parse_tree(filename):
        G = nx.DiGraph()
        parentChildMap = {}
        lineCounter = 1
        parent = None
        prevCounter = 0
        prevObj = None
        root = None
        with open(filename, "r") as f:
            for line in f:
                currentCounter = 0
                if not (line.startswith("Input") or line.startswith("Parse")):
                    arr=[]
                    if('punct' in line):
                        arr = re.split('(\W)', line)
                        for x in arr:
                            if x in (' ', '|', '+', '-', '\n'):
                                arr.remove(x);
                    else:
                        arr = re.split('\W', line)
                    if(arr[-1] == ''):
                        del arr[-1]
                    usefulArr = []
                    for x in arr:
                        if not x:
                            currentCounter+=1
                        else:
                            usefulArr.append(x)
                    if('punct' in line):
                        currentCounter = currentCounter-4
                    obj = Node(usefulArr[0], usefulArr[1], usefulArr[2]);
                    if lineCounter == 1:
                        parent = obj
                        prevObj = obj
                        root = obj
                        G.add_node(root, word=root.word, POS=root.POS, attr=root.attribute)
                        lineCounter = -1

                    if prevCounter != currentCounter:
                         parent = prevObj
                         if currentCounter in parentChildMap and currentCounter > prevCounter:
                             parentChildMap[currentCounter] = parent


                    if currentCounter in parentChildMap:
                        parent = parentChildMap[currentCounter]

                    elif currentCounter not in parentChildMap:
                        parentChildMap[currentCounter] = parent

                    G.add_node(obj, word=obj.word, POS=obj.POS, attr=obj.attribute)
                    G.add_edge(parent, obj)
                    parent.add_child(obj)
                    prevCounter = currentCounter
                    prevObj = obj
        return root, G