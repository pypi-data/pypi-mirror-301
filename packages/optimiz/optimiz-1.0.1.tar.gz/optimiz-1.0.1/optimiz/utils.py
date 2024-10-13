

"""Utility functions"""
import numpy as np
from .losses import mse_loss

def _compute_gradient(X, y, weights):
    m = len(y)
    predictions = X.dot(weights)
    gradient = (1 / m) * X.T.dot(predictions - y)
    return gradient

def mse_partial_gradient(X, y, weights, j):
    """
    Computes the partial gradient of the MSE loss with respect to weight j.

    Args:
        X (numpy.ndarray): The input feature matrix.
        y (numpy.ndarray): The true target values.
        weights (numpy.ndarray): The current weights.
        j (int): The index of the weight to compute the gradient for.

    Returns:
        float: The computed partial gradient.
    """
    m = len(y)
    return (1 / m) * np.sum((X @ weights - y) * X[:, j])

def print_details(iterations , weights , y ,X):
    print(f"Iteration : {iterations} , Loss : {mse_loss(y, X.dot(weights))} ")

    