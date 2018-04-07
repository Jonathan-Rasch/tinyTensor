'''
Nodes can be variables ,placeholders or operations.
'''
import tinyTensor.Graph

class Node():

    # variable node constructor
    def __init__(self):
        self.value = None
        self.isPlaceholder = False
        self.name = ""
        self.inputNodes = []

    @classmethod
    def variable(cls,value):
        if (value == None):
            raise Exception("A variable node cannot have a value of 'None'")
        variableNode = Node()
        variableNode.value = value
        variableNode.isPlaceholder = False
        tinyTensor.Graph._default_graph.appendNode(variableNode)
        return variableNode

    @classmethod
    def placeholder(cls,name):
        if(name == None):
            raise Exception("Placeholders need to be assigned a unique name to allow their value to be changed via feed dictionary.")
        placeholderNode = Node()
        placeholderNode.name = name
        placeholderNode.isPlaceholder = True
        tinyTensor.Graph._default_graph.appendNode(placeholderNode)
        return placeholderNode

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




