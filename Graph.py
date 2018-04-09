#from tinyTensor.Node import Node
import tinyTensor
import plotly.plotly as py
from graphviz import render
#from tinyTensor.Operation import Operation


def init():
    global _default_graph
    _default_graph = None

def postOrder(node):
    nodes_postorder = []
    def recurse(node):
        if isinstance(node, tinyTensor.Node.Node):
            for input_node in node.inputNodes:
                recurse(input_node)
            nodes_postorder.append(node)
    recurse(node)
    return nodes_postorder

class Graph():

    def __init__(self):
        self.nodes = []
        self.placeholderNames = []

    def appendNode(self,node):
        if(node.name in self.placeholderNames and node.isPlaceholder):
            raise Exception("Placeholder name \"{}\" is already in use in current graph".format(node.name))
        elif(node.isPlaceholder):
            self.placeholderNames.append(node.name)
        self.nodes.append(node)

    def set_default(self):
        init()
        global _default_graph
        _default_graph = self

    def visualize_nodes(self, node):
        # generating the .gv file
        gv_file = "graph \"\" \n{\n"
        global nodeCounter
        nodeCounter = 0
        def recurse(nodes,gv_file,parent_node_str = None):
            global nodeCounter
            nodes_list = []
            if(isinstance(nodes,list)):
                nodes_list.extend(nodes)
            else:
                nodes_list.append(nodes)
            for node in nodes_list:
                # node should add itself to the list
                current_node_str = "n" + str(nodeCounter)
                nodeCounter += 1
                ''' operation might contain non-node constants, hence need to make sure that they are converted to node'''
                if(type(node) in (int,float)):
                    node = tinyTensor.Node.Node.variable(node) # creating a variable node
                '''creating the node labels'''
                if(isinstance(node,tinyTensor.Operation.Operation)):
                    gv_file += current_node_str + " [label=\"{} ({})\"] ;\n".format(node.operator,node.value)
                elif(node.isPlaceholder):
                    gv_file += current_node_str + " [label=\"{}({})\"] ;\n".format(node.name,node.value)
                else:
                    gv_file += current_node_str + " [label=\"{}({})\"] ;\n".format(node.name,node.value)
                # now creating connection line to parent(s) TODO: make it possible to have many parents, (nodes should have output nodes list)
                if(parent_node_str != None):
                    gv_file += parent_node_str + " -- " + current_node_str + "; \n"
                # applying the same to the children of this node
                if(len(node.inputNodes) > 0):
                    gv_file = recurse(node.inputNodes,gv_file,current_node_str)
            return gv_file
        gv_file = recurse(node,gv_file)
        gv_file += "}\n"
        with open("network.gv","w+") as file:
            file.writelines(gv_file)
        #render('dot','png','network.gv')
        print(gv_file)

    def visualize_layers(self,layer_list):
        neuron_dict = {}
        #generating dict of neurons
        gv_file = "graph \"\" \n{\n"
        #dealing with input nodes
        for node in layer_list[0].inputList:
            neuron_dict[node] = node.name
            gv_file += neuron_dict[node] + " [label=\"{}\"] ;\n".format(node.name)
        # creating dict for neurons
        for layer in layer_list:
            for neuron in layer.neuronList:
                neuron_dict[neuron] = "{}".format(neuron.name)
                gv_file += neuron_dict[neuron] + " [label=\"{}\"] ;\n".format(neuron.name)
        # drawing links between neurons
        for layer in layer_list:
            for neuron in layer.neuronList:
                for input_neuron in neuron.inputNeurons:
                    gv_file += neuron_dict[neuron] + " -- " + neuron_dict[input_neuron] + "; \n"
        gv_file += "}\n"
        with open("network.gv","w+") as file:
            file.writelines(gv_file)
        print(gv_file)




