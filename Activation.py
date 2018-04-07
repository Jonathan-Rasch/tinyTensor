from tinyTensor.Node import Node
import numpy as np
import tinyTensor.Graph

class Act(Node):

    def __init__(self, function: str, node: Node) -> Node:
        """
        :param function: name of activation function to be used
        :param node: node to which the activation function is applied at its output
        """
        super().__init__()
        if(function.lower() == "sigmoid"):
            self.function = self.sigmoid
            self.name = "Sigm"
        elif(function.lower() == "tanh"):
            self.function = self.tanh
            self.name = "tanh"
        elif(function.lower() == "relu"):
            self.function = self.relu
            self.name = "ReLu"
        elif(function.lower() == "step"):
            self.function = self.step
        else:
            raise Exception("Unknown activation function \"{}\"".format(function))
        # input(s) to this node
        self.inputNodes = [node]
        # adding node to the graph
        tinyTensor.Graph._default_graph.appendNode(self)

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
