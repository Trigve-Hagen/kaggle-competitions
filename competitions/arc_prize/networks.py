# https://www.youtube.com/watch?v=tMrbN67U9d4&list=PLQVvvaa0QuDcjD5BAw2DxE6OF2tius3V3

import numpy as np

# layers
""" inputs = [1, 2, 3, 2.5]
weights = [
  [0.2, 0.8, -0.5, 1.0],
  [0.5, -0.91, 0.26, -0.5],
  [-0.26, -0.27, 0.17, 0.87]
]
biases =[2, 3, 0.5]

layer_outputs = [] # Output of current layer
for neuron_weights, neuron_bias in zip(weights, biases):
  neuron_output = 0 # Output of given neuron
  for n_input, weights in zip(inputs, neuron_weights):
    neuron_output += n_input * weights
  neuron_output += neuron_bias
  layer_outputs.append(neuron_output)

print(layer_outputs)
# outputs: [4.8, 1.21, 2.385] """


# dot product
# Key take away is dot product is the same calculation as the forward pass calculation
# on a neuron
""" inputs = [1, 2, 3, 2.5]
weights = [0.2, 0.8, -0.5, 1.0]
bias = [2]

output = np.dot(weights, inputs) + bias
print(output)
# outputs: 4.8 """

""" inputs = [1, 2, 3, 2.5]
weights = [
  [0.2, 0.8, -0.5, 1.0],
  [0.5, -0.91, 0.26, -0.5],
  [-0.26, -0.27, 0.17, 0.87]
]
biases =[2, 3, 0.5]

# with np.dot the first (element)parameter you pass is how the return will be
# indexed. Since weights are defining the number of neurons we want the weights
# to define the way the return will be indexed. Also in dot product multiplication
# you need to be careful that the shape is right or it throws errors.
output = np.dot(weights, inputs) + biases
print(output)
# outputs: [4.8, 1.21, 2.385] """

# batches
""" inputs = [
  [1, 2, 3, 2.5],
  [2.0, 5.0, -1.0, 2.0],
  [-1.5, 2.7, 3.3, -0.8]
]
npinputs = np.array(inputs)
# print(npinputs.shape)
# outputs: (3, 4)

weights = [
  [0.2, 0.8, -0.5, 1.0],
  [0.5, -0.91, 0.26, -0.5],
  [-0.26, -0.27, 0.17, 0.87]
]
npweights = np.array(weights)
# print(npweights.shape)
# outputs: (3, 4)

biases =[2, 3, 0.5]

# The number of columns in the first matrix must equal the number of rows
# in the second matrix.
# Example: (1, 5) dot (5, 3) -> (1, 3)
# since the weights and inputs shape will throw a shape error the way they are
# weights: (3, 4) dot (3, 4) -> Shape error
# we need to transpose the weights
output = np.dot(inputs, np.array(weights).T) + biases
print(output)
# outputs: [[ 4.8    1.21   2.385]
# [ 8.9   -1.81   0.2  ]
# [ 1.41   1.051  0.026]] """

# layers
""" inputs = [
  [1, 2, 3, 2.5],
  [2.0, 5.0, -1.0, 2.0],
  [-1.5, 2.7, 3.3, -0.8]
]

weights = [
  [0.2, 0.8, -0.5, 1.0],
  [0.5, -0.91, 0.26, -0.5],
  [-0.26, -0.27, 0.17, 0.87]
]
biases =[2, 3, 0.5]

weights2 = [
  [0.1, -0.14, 0.5],
  [-0.5, 0.12, -0.33],
  [-0.44, 0.73, -0.13]
]
biases2 =[-1, 2, -0.5]

layer1_outputs = np.dot(inputs, np.array(weights).T) + biases
layer2_outputs = np.dot(layer1_outputs, np.array(weights2).T) + biases2
print(layer2_outputs)
# outputs: [[ 0.5031  -1.04185 -2.03875]
#  [ 0.2434  -2.7332  -5.7633 ]
#  [-0.99314  1.41254 -0.35655]] """

# objects
X = [
  [1, 2, 3, 2.5],
  [2.0, 5.0, -1.0, 2.0],
  [-1.5, 2.7, 3.3, -0.8]
]
np.random.seed(0)

# The data saved in a model is weights and biases.
class LayerDense:

  def __init__(self, n_input, n_neurons):
    self.weights = 0.10 * np.random.randn(n_input, n_neurons)
    self.biases = np.zeros((1, n_neurons))

  def forward(self, inputs):
    self.output = np.dot(inputs, self.weights) + self.biases

layer1 = LayerDense(4, 5)
layer2 = LayerDense(5, 2)

layer1.forward(X)
layer2.forward(layer1.output)
print(layer2.output)




