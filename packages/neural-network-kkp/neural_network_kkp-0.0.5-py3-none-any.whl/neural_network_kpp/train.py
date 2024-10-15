import numpy as np


def train(network, X, y, loss_func, epochs, batch_size=32):
    num_samples = X.shape[0]

    for epoch in range(epochs):

        indices = np.random.permutation(num_samples)
        X_shuffled = X[indices]
        y_shuffled = y[indices]

        for start in range(0, num_samples, batch_size):
            end = start + batch_size
            batch_X = X_shuffled[start:end]
            batch_y = y_shuffled[start:end]

            network.backward(batch_X, batch_y, loss_func)

        loss_value = loss_func(y, network.forward(X))
        print(f"Эпоха {epoch + 1}/{epochs}, Потеря: {loss_value:.4f}")
