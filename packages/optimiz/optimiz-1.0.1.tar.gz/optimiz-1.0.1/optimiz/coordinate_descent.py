import numpy as np
from .optimizer import Optimizier
from .losses import mse_loss
import random
from .utils import mse_partial_gradient

class CoordinateDescent(Optimizier):
    """
    Coordinate Descent optimization algorithm.

    Args:
        learning_rate (float): The step size for weight updates.
        iterations (int): The number of iterations to perform.
        tolerance (float): The tolerance for stopping criteria.
    """

    def __init__(self, learning_rate, iterations, tolerance , method = None) -> None:
        """
        Initializes the CoordinateDescent optimizer.

        Args:
            learning_rate (float): The step size for weight updates.
            iterations (int): The number of iterations to perform.
            tolerance (float): The tolerance for stopping criteria.
        """
        super().__init__(learning_rate, iterations, tolerance)
        self.method = method

    def optimize(self, X, y, initial_weights=None):
        """
        Performs the optimization process using Coordinate Descent.

        Args:
            X (numpy.ndarray): The input feature matrix.
            y (numpy.ndarray): The target values.
            initial_weights (numpy.ndarray, optional): Initial weights for optimization.

        Returns:
            numpy.ndarray: The optimized weights after the process.
        """
        m, n = X.shape
        weights = initial_weights.copy()
        loss_history = []

        for i in range(self.iterations):
            if self.method=="cyclic" or self.method == None:
                for j in range(n):
                    partial_j_gradient = mse_partial_gradient(X, y, weights, j)
                    weights[j] -= self.learning_rate * partial_j_gradient

            elif self.method=="random":
                j = random.randint(0 , n-1)
                partial_j_gradient = mse_partial_gradient(X , y ,weights , j)
                weights[j] -= self.learning_rate * partial_j_gradient
            
            elif self.method=="greedy":
                 gradients = np.array([mse_partial_gradient(X , y , weights , j) for j in range(n)])
                 j_argmax = np.argmax(np.abs(gradients))
                 weights[j_argmax] -= self.learning_rate * gradients[j_argmax]

            loss = mse_loss(y , X.dot(weights))
            loss_history.append(loss)

            if i % 100 == 0:
                    print(f"Iteration : {i} , Loss : {loss} ")

        return weights , loss_history