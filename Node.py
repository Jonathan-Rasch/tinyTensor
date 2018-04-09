'''
Nodes can be variables ,placeholders or operations.
'''
import random

import tinyTensor.Graph

class Node():

    # variable node constructor
    def __init__(self):
        self.value = None
        self.isPlaceholder = False
        self.isDropout = False
        self.isDropoutActive = False # dropout should only be active during training.
        self.dropoutPercentage = 0
        self.name = ""
        self.inputNodes = []
        self.step = 0 # the current learning / computation step (prevents nodes being computed twice or more)

    @classmethod
    def variable(cls,value,name=""):
        if (value == None):
            raise Exception("A variable node cannot have a value of 'None'")
        variableNode = Node()
        variableNode.value = value
        variableNode.name = name
        tinyTensor.Graph._default_graph.appendNode(variableNode)
        return variableNode

    @classmethod
    def placeholder(cls,name,value=None):
        if(name == None):
            raise Exception("Placeholders need to be assigned a unique name to allow their value to be changed via feed dictionary.")
        placeholderNode = Node()
        placeholderNode.name = name
        placeholderNode.value = value
        placeholderNode.isPlaceholder = True
        tinyTensor.Graph._default_graph.appendNode(placeholderNode)
        return placeholderNode

    @classmethod
    def dropout(cls,dropout_percentage: float = 0):
        if(dropout_percentage > 1 or dropout_percentage < 0):
            raise Exception("invalid dropout percentage {}, value needs to be between 0 and 1 (inclusive)")
        dropoutNode = Node()
        dropoutNode.name = "dropout"
        dropoutNode.isDropout = True
        dropoutNode.dropoutPercentage = dropout_percentage
        tinyTensor.Graph._default_graph.appendNode(dropoutNode)
        return dropoutNode

    def compute(self,step):
        if (self.step == step):
            return self
        else:
            self.step = step
        if(self.isDropout):
            random.seed()
            rand = random.randrange(1001)/1000
            if(rand < self.dropoutPercentage):
                print("DROP {}:{}".format(self.dropoutPercentage,rand))
                self.value = 0
            else:
                print("OK {}:{}".format(self.dropoutPercentage, rand))
                self.value = self.inputNodes[0].value
        return self

    def addInputs(self,nodes):
        if(not isinstance(nodes,list)):
            nodes = [nodes]
        if(not all(isinstance(x,Node) for x in nodes)):
            raise Exception("nodes parameter should be a list of objects of type Node")
        elif(self.isDropout and ((len(nodes) + len(self.inputNodes)) != 1)):
            raise Exception("dropout nodes need to have 1 and only 1 input.")
        self.inputNodes.extend(nodes)

    def setInputs(self,nodes):
        self.inputNodes.clear()
        self.addInputs(nodes)

    def __add__ (self,other):
        operation = tinyTensor.Operation.Operation([self, other], "+")
        return operation

    def __sub__ (self,other):
        operation = tinyTensor.Operation.Operation([self, other], "-")
        return operation

    def __mul__ (self,other):
        operation = tinyTensor.Operation.Operation([self, other], "*")
        return operation

    def __truediv__ (self,other):
        operation = tinyTensor.Operation.Operation([self, other], "/")
        return operation

    def __mod__ (self,other):
        operation = tinyTensor.Operation.Operation([self, other], "%")
        return operation




