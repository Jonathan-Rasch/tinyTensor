from tinyTensor.Graph import Graph
from tinyTensor.Node import Node
from tinyTensor.Session import Session

g = Graph()
g.set_default()
a = Node.variable(value=8.0)
b = Node.variable(value=2.5)
x = Node.placeholder(name="x")
c = Node.variable(2)
z = ((a*x + b)*c) / 5

session = Session()
result = session.run(node=z,feed_dict={"x":10})
print(result)