import numpy as np
from .activations import ReLU, Sigmoid, Tanh


class Initializer:
    @staticmethod
    def initialize_weights(input_size, output_size, method='random'):
        if method == 'random':
            return np.random.randn(input_size, output_size) * 0.01
        elif method == 'xavier':
            return np.random.randn(input_size, output_size) * np.sqrt(1 / input_size)
        elif method == 'he':
            return np.random.randn(input_size, output_size) * np.sqrt(2 / input_size)
        elif method == 'normal':
            return np.random.normal(0, 1, (input_size, output_size))
        else:
            raise ValueError(f"Ошибка: {method}")

    @staticmethod
    def initialize_biases(output_size, method='zeros'):
        if method == 'zeros':
            return np.zeros((1, output_size))
        elif method == 'ones':
            return np.ones((1, output_size))
        elif method == 'normal':
            return np.random.normal(0, 1, (1, output_size))
        else:
            raise ValueError(f"Ошибка: {method}")


class DenseLayer:
    def __init__(self, input_size, output_size, activation_func, weights_initializer='random',
                 biases_initializer='zeros', learning_rate=0.01):
        self.activation_func = activation_func
        self.learning_rate = learning_rate
        self.weights = Initializer.initialize_weights(input_size, output_size, weights_initializer)
        self.biases = Initializer.initialize_biases(output_size, biases_initializer)

    def forward(self, inputs):
        self.inputs = inputs
        self.z = np.dot(inputs, self.weights) + self.biases
        self.a = self.activation_func(self.z)
        return self.a

    def backward(self, grad_output):
        grad_activation = self.activation_func.derivative(self.z)
        grad_input = np.dot(grad_output * grad_activation, self.weights.T)
        grad_weights = np.dot(self.inputs.T, grad_output * grad_activation)
        grad_biases = np.sum(grad_output * grad_activation, axis=0, keepdims=True)

        self.weights -= self.learning_rate * grad_weights
        self.biases -= self.learning_rate * grad_biases

        return grad_input
