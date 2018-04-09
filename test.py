from tinyTensor.Layer import Layer
from tinyTensor.Graph import Graph
from tinyTensor.Neuron import Neuron
from tinyTensor.Node import Node
from tinyTensor.Session import Session
from tinyTensor.Operation import Operation as op
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

# g = Graph()
# g.set_default()
# a = Node.variable(value=8.0)
# b = Node.variable(value=2.5)
# x = Node.placeholder(name="x")
# c = Node.variable(2)
# z = (((a*x + b)*c) / 5) + (a*x*b + x) + (Node.variable(500) + op.relu_act((a*(b+c))) % (a+b+c+x) + op.sum(a,b,c,x))
#
# session = Session()
# result = session.run(node=z,feed_dict={"x":10})
# print(result)
# g.visualize(z)

########################################################################################################################
# SIMPLE CLASSIFICATION TEST
########################################################################################################################

# data = make_blobs(n_samples=500,n_features=2,centers=2,random_state=75,cluster_std=3)
# features = data[0]
# labels = data[1]
# #plt.scatter(features[:,0],features[:,1],c=labels)
# #plt.show()
#
# g2 = Graph()
# session2 = Session()
# g2.set_default()
# var1 = Node.variable(0.9)
# var2 = Node.variable(0.1)
# var3 = Node.variable(0.0)
# var4 = Node.variable(0.6)
# var5 = Node.variable(0.4)
# var6 = Node.variable(0.7)
# varList = [var1,var2,var3,var4,var5,var6]
# n1 = Neuron(varList,activation_fnct="relu",dropout=0.3)
# n2 = Neuron(varList,activation_fnct="relu",dropout=0.3)
# n3 = Neuron(varList,activation_fnct="relu",dropout=0.3)
# n4 = Neuron(varList,activation_fnct="relu",dropout=0.3)
# layer1 = [n1,n2,n3,n4]
# n5 = Neuron(layer1,activation_fnct="relu",dropout=0.3)
# n6 = Neuron(layer1,activation_fnct="relu",dropout=0.3)
# n7 = Neuron(layer1,activation_fnct="relu",dropout=0.3)
# layer2 = [n5,n6,n7]
# n8 = Neuron(layer2,activation_fnct="relu",dropout=0.3)
# print(session2.run(n8,{}))
# g2.visualize(n8)

g3 = Graph()
g3.set_default()
inputs = [Node.variable(0,"v0"),Node.variable(1,"v1"),Node.variable(2,"v2"),Node.variable(3,"v3"),Node.variable(4,"v4"),Node.variable(5,"v5")]
layer1 = Layer(inputs,10,"relu",0)
layer2 = Layer(layer1.neuronList,5,"relu",0)
layer3 = Layer(layer2.neuronList,1,"relu",0)
g3.visualize_layers([layer1,layer2,layer3])

