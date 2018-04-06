from tinyTensor.Node import Node

def init():
    global _default_graph
    _default_graph = None

class Graph():

    def __init__(self):
        self.nodes = []
        self.placeholderNames = []

    def appendNode(self,node: Node):
        if(node.name in self.placeholderNames and node.isPlaceholder):
            raise Exception("Placeholder name \"{}\" is already in use in current graph".format(node.name))
        self.nodes.append(node)
        self.placeholderNames.append(node.name)

    def set_default(self):
        init()
        global _default_graph
        _default_graph = self