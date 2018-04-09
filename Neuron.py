from tinyTensor.Operation import Operation
from tinyTensor.Node import Node
import tinyTensor.Graph
import random as rand

class Neuron(Node):

    def __init__(self, input_neurons: list = [], activation_fnct: str = "relu", dropout: float = 0.0):
        super().__init__()
        self.name = "Neuron output"
        # input validation
        if( not all(isinstance(x,Node) for x in input_neurons)):
            raise Exception("'input_neurons' list (parameter) should only contain objects of type 'Node'.")
        elif(dropout > 1 or dropout < 0):
            raise Exception("'dropout' (parameter) should have a value between 0(inclusive) and 1(inclusive).")
        self.activation = activation_fnct
        self.dropout_percentage = dropout
        self.inputNeurons = input_neurons
        ########################################################################################################################
        # Neuron structure
        ########################################################################################################################
        self.weighted_inputs = []
        self.input_weights = []
        # bias input, and normal weighted neuron inputs
        self.input_weights.append(Node.variable(rand.randrange(-1000, 1000)/1000))
        self.weighted_inputs.append(self.input_weights[0] * -1)
        for index,node in enumerate(input_neurons):
            index = index + 1  # bias of neuron is at index 0, so need to shift by 1
            self.input_weights.append(Node.variable(rand.randrange(-1000, 1000)/1000))  # random initialisation of input weights
            self.weighted_inputs.append(self.input_weights[index] * node)
        # computing weighted sum of inputs
        self.weighted_sum_of_inputs = Operation.sum(self.weighted_inputs)
        # activation function
        self.activation_function = Operation(self.weighted_sum_of_inputs,"relu")
        # dropout
        if(self.dropout_percentage > 0):
            self.dropoutNode = Node.dropout(dropout)
            self.dropoutNode.addInputs(self.activation_function)
            self.inputNodes = [self.dropoutNode]
        else:
            self.inputNodes = [self.activation_function]
        tinyTensor.Graph._default_graph.appendNode(self)

    def compute(self):
        self.value = self.inputNodes[0].value
        return





