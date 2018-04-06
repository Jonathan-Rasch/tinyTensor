from tinyTensor.Node import Node
import numpy as np
import typing
'''
This class is created by the node class when an operation is performed on two nodes.

'''
class Operation(Node):

    def __init__(self, operandA: Node, operandB: Node, operator: str) -> None:
        super().__init__()
        if(not operator in ['+','-','/','*','%']):
            raise Exception('invalid operator provided: {0}'.format(operator))
        elif(operandA == None or operandB == None):
            raise Exception('provided operands cannot be None.')
        self.operator = operator

        if(not isinstance(operandA,Node) and type(operandA) in [int,float]):
            self.NodeA = Node.variable(operandA)
        else:
            self.NodeA = operandA

        if (not isinstance(operandB, Node) and type(operandB) in [int, float]):
            self.NodeB = Node.variable(operandB)
        else:
            self.NodeB = operandB

        self.inputNodes = [operandA,operandB]

    def compute(self) -> Node:
        if(self.operator == "+"):
            self.value = self.NodeA.value + self.NodeB.value
        elif(self.operator == "-"):
            self.value = self.NodeA.value - self.NodeB.value
        elif (self.operator == "/"):
            self.value = self.NodeA.value / self.NodeB.value
        elif (self.operator == "%"):
            self.value = self.NodeA.value % self.NodeB.value
        elif (self.operator == "*"):
            self.value = self.NodeA.value * self.NodeB.value
        else:
            raise Exception("Unknown operator: {0}".format(self.operator))
        return self