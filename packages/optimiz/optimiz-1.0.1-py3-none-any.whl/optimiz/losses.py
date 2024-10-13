import numpy as np

def mse_loss(y_true, y_pred):
    """
    Computes the Mean Squared Error (MSE) loss.

    Args:
        y_true (numpy.ndarray): The true target values.
        y_pred (numpy.ndarray): The predicted target values.

    Returns:
        float: The computed MSE loss.
    """
    mse = (1 / 2) * np.mean((y_true - y_pred) ** 2)
    return mse

def mse_gradient(X, y_true, y_pred):
    """
    Computes the gradient of the MSE loss.

    Args:
        X (numpy.ndarray): The input feature matrix.
        y_true (numpy.ndarray): The true target values.
        y_pred (numpy.ndarray): The predicted target values.

    Returns:
        numpy.ndarray: The computed gradient.
    """
    m = len(y_true)
    gradient = (1 / m) * X.T.dot(y_pred - y_true)
    return gradient

# def mse_partial_gradient(X, y, weights, j):
#     """
#     Computes the partial gradient of the MSE loss with respect to weight j.

#     Args:
#         X (numpy.ndarray): The input feature matrix.
#         y (numpy.ndarray): The true target values.
#         weights (numpy.ndarray): The current weights.
#         j (int): The index of the weight to compute the gradient for.

#     Returns:
#         float: The computed partial gradient.
#     """
#     m = len(y)
#     return (1 / m) * np.sum((X @ weights - y) * X[:, j])