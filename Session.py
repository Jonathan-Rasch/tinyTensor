from tinyTensor.Node import Node
from tinyTensor.Operation import Operation
import numpy as np

def postOrder(operation):
    nodes_postorder = []
    def recurse(node):
        if isinstance(node, Node):
            for input_node in node.inputNodes:
                recurse(input_node)
            nodes_postorder.append(node)
    recurse(operation)
    return nodes_postorder

class Session():

    def run(self,node: Node,feed_dict={}):
        nodes_postOrder = postOrder(node)
        for node in nodes_postOrder:
            if node.isPlaceholder:
                node.value = feed_dict[node.name]
            elif isinstance(node,Operation):
                #node.inputNodes = [input_node.value for input_node in node.inputNodes]
                node.output = node.compute()#*node.inputNodes)
            if(type(node.value) == list):
                node.output = np.array(node.output)
        return node.value