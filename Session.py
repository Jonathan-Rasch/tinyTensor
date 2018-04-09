from tinyTensor import Neuron
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
                # placeholders need value from feed dict
                node.value = feed_dict[node.name]
            node.compute(step=1)
        return node.value