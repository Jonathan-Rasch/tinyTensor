from tinyTensor.Node import Node
import numpy as np
import typing
import tinyTensor.Graph
'''
This class is created by the node class when an operation is performed on two nodes.

'''
class Operation(Node):

    def __init__(self, nodes, operator: str) -> None:
        super().__init__()
        if(not isinstance(nodes,list)):
            raise Exception("nodes argument needs to be a LIST of nodes")
        if(len(nodes) > 2): # oparation on a range of nodes
            if (not operator in ['sum','mean']):
                raise Exception('invalid operation: {0}'.format(operator))
            self.inputNodes = nodes
            self.name = operator
            self.operator = operator
        else: # simple operation on two nodes
            operandA = nodes[0]
            operandB = nodes[1]
            if(not operator in ['+','-','/','*','%']):
                raise Exception('invalid operator provided: {0}'.format(operator))
            elif(operandA == None or operandB == None):
                raise Exception('provided operands cannot be None.')
            self.operator = operator
            self.name = operator
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

    @classmethod
    def sum(cls,*argv):
        nodes = Operation.extractAndValidate(argv)
        op = Operation(nodes=nodes,operator="sum")
        return op

    @staticmethod
    def extractAndValidate(argv):
        """
        extracts nodes from argv passed into function
        :param argv:
        """
        nodes = []
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


    def compute(self) -> Node:
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
        else:
            raise Exception("Unknown operator: {0}".format(self.operator))
        return self