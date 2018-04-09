from tinyTensor.Neuron import Neuron

global _neuron_counter
_neuron_counter = 0

class Layer():

    def __init__(self, inputs, neuron_number, activation_fnct, dropout_percentage):
        global _neuron_counter
        self.neuronList = []
        self.inputList = inputs
        for n in range(0,neuron_number):
            neuron = Neuron(inputs,activation_fnct,dropout_percentage)
            neuron.name = "N"+str(_neuron_counter)
            self.neuronList.append(neuron)
            _neuron_counter += 1