from tinyTensor.Node import Node
import numpy as np
import typing
import tinyTensor.Graph
'''
This class is created by the node class when an operation is performed on two nodes, or when the
user uses one of the named functions that operation supports (e.g. sum or mean)
'''

oneParamFunctionList = ['sigmoid', 'tanh','relu','step']
onePlusParamFunctList = ['sum', 'mean']
twoParamFunctionList = ['+', '-', '/', '*', '%']
class Operation(Node):

    def __init__(self, nodes, function: str) -> None:
        super().__init__()
        if(not isinstance(nodes,list)):
            nodes = [nodes]
        if(len(nodes) > 2): # oparation on a range of nodes
            if (not function in onePlusParamFunctList ):
                raise Exception('invalid operation: {0}'.format(function))
            self.inputNodes = nodes
            self.name = function
            self.operator = function
        elif(len(nodes) == 2): # simple operation on two nodes
            operandA = nodes[0]
            operandB = nodes[1]
            if(not function in twoParamFunctionList):
                raise Exception('invalid operator provided: {0}'.format(function))
            elif(operandA == None or operandB == None):
                raise Exception('provided operands cannot be None.')
            self.operator = function
            self.name = function
            tinyTensor.Graph._default_graph.appendNode(self)

            if(not isinstance(operandA,Node) and type(operandA) in [int,float]):
                self.NodeA = Node.variable(operandA)
            else:
                self.NodeA = operandA

            if (not isinstance(operandB, Node) and type(operandB) in [int, float]):
                self.NodeB = Node.variable(operandB)
            else:
                self.NodeB = operandB
            self.inputNodes = [operandA,operandB]
        elif(len(nodes) == 1): # single node operations, e.g activation functions
            if (not function in oneParamFunctionList + onePlusParamFunctList):
                raise Exception('invalid operation: {0}'.format(function))
            self.inputNodes = nodes
            self.name = function
            self.operator = function

    """'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    NAMED OPERATIONS
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''"""

    @classmethod
    def sum(cls,*argv):
        nodes = Operation.extractAndValidate(argv)
        op = Operation(nodes=nodes, function="sum")
        return op

    @classmethod
    def mean(cls,*argv):
        nodes = Operation.extractAndValidate(argv)
        op = Operation(nodes=nodes, function="mean")
        return op

    @staticmethod
    def extractAndValidate(argv):
        """
        extracts nodes from argv passed into function
        :param argv:
        """
        nodes = []
        if(not isinstance(argv,list) and not isinstance(argv,tuple)):
            argv = [argv]
        for arg in argv:
            # some basic input validation
            if (arg == None):
                raise Exception("Input node to operation cannot be of type NONE")
            elif(type(arg) in (int,float)): # const needs to be converted to Node
                tmpNode = Node.variable(arg)
                nodes.append(tmpNode)
            elif(isinstance(arg,Node)):
                nodes.append(arg)
            elif(isinstance(arg,list)): # dealing with lists of nodes passed into operation
                for node in arg:
                    extracted = Operation.extractAndValidate(node)
                    if(isinstance(extracted,list)):
                        nodes.extend(extracted)
                    else:
                        nodes.append(extracted)
            else:
                raise Exception("Argument provided is not of type Node")
        return nodes

    """'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ACTIVATION FUNCTIONS
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''"""

    @classmethod
    def sigmoid_act(cls, *argv):
        nodes = Operation.extractAndValidate(argv)
        op = Operation(nodes=nodes, function="sigmoid")
        return op

    @classmethod
    def tanh_act(cls, *argv):
        nodes = Operation.extractAndValidate(argv)
        op = Operation(nodes=nodes, function="tanh")
        return op

    @classmethod
    def relu_act(cls, *argv):
        nodes = Operation.extractAndValidate(argv)
        op = Operation(nodes=nodes, function="relu")
        return op

    @classmethod
    def step_act(cls, *argv):
        nodes = Operation.extractAndValidate(argv)
        op = Operation(nodes=nodes, function="step")
        return op

    def sigmoid(self,value):
        return 1 / (1 + np.exp(-value))

    def tanh(self,value):
        return np.tanh(value)

    def relu(self,value):
        if(value < 0):
            return 0
        else:
            return value

    def step(self,value):
        if(value<0):
            return -1
        else:
            return 1

    """'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    COMPUTE
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''"""

    def compute(self,step) -> Node:
        if (self.step == step):
            return self
        else:
            self.step = step
        if (self.operator == "+"):
            self.value = self.NodeA.value + self.NodeB.value
        elif (self.operator == "-"):
            self.value = self.NodeA.value - self.NodeB.value
        elif (self.operator == "/"):
            self.value = self.NodeA.value / self.NodeB.value
        elif (self.operator == "%"):
            self.value = self.NodeA.value % self.NodeB.value
        elif (self.operator == "*"):
            self.value = self.NodeA.value * self.NodeB.value
        elif (self.operator == "sum"):
            self.value = 0
            for node in self.inputNodes:
                self.value += node.value
        elif (self.operator == "mean"):
            self.value = 0
            for node in self.inputNodes:
                self.value += node.value
            self.value /= len(self.inputNodes)
        elif(self.operator == "sigmoid"):
            self.value = self.sigmoid(self.inputNodes[0].value)
        elif (self.operator == "tanh"):
            self.value = self.tanh(self.inputNodes[0].value)
        elif (self.operator == "relu"):
            self.value = self.relu(self.inputNodes[0].value)
        elif (self.operator == "step"):
            self.value = self.step(self.inputNodes[0].value)
        else:
            raise Exception("Unknown operator: {0}".format(self.operator))
        return self