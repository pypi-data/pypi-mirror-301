from .optimizer import Optimizier
import random
import numpy as np
from .gradient_descent import GradientDescent
from .losses import mse_loss
from .utils import _compute_gradient

class StocasticGradientDescent(Optimizier):

    def __init__(self, learning_rate, iterations, tolerance , batch_size=1) -> None:
        super().__init__(learning_rate, iterations, tolerance)
        #self.gradient_descent = GradientDescent(learning_rate=learning_rate, iterations=iterations , tolerance=tolerance)
        self.batch_size = batch_size
    
    def optimize(self , X , y , initial_weights=None ):
        
        m, n = X.shape
        weights = initial_weights.copy()
        loss_history = []
        for i in range(1 , self.iterations+1):
            idxs = np.arange(m)
            #shuffling the index
            np.random.shuffle(idxs)
            X = X[idxs]
            y = y[idxs]

            for j in range(0 , m , self.batch_size):
                X_batch = X[j : j + self.batch_size]
                y_batch = y[j : j + self. batch_size]
                gradient = _compute_gradient(X_batch , y_batch , weights)
                weights -= self.learning_rate * gradient
            loss = mse_loss(y ,np.dot(X , weights))
            loss_history.append(loss)
            if i % 100 == 0:
                print(f"Iteration : {i} , Loss : {mse_loss(y , X.dot(weights))}")
            
        return weights , loss_history 


    
    # def _compute_gradient(self, X, y, weights):
    #     """
    #     Computes the gradient for the given weights.

    #     Args:
    #         X (numpy.ndarray): The input feature matrix.
    #         y (numpy.ndarray): The target values.
    #         weights (numpy.ndarray): The current weights.

    #     Returns:
    #         numpy.ndarray: The computed gradient.
    #     """
    #     m = len(y)
    #     predictions = X.dot(weights)
    #     gradient = (1 / m) * X.T.dot(predictions - y)
    #     return gradient