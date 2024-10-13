from .optimizer import Optimizier
from .utils import _compute_gradient , print_details
import numpy as np
from .utils import mse_loss

"""Ref : https://paperswithcode.com/method/nesterov-accelerated-gradient"""

class NesterovAcceleratedGradientDescent(Optimizier):

    def __init__(self, learning_rate=None, iterations=None, tolerance=None , beta = 0.9) -> None:
        super().__init__(learning_rate, iterations, tolerance)
        self.beta = 0.9

    def optimize(self , X , y , initial_weights):

        weights = initial_weights.copy()
        v = np.zeros_like(weights)
        loss_history = []

        for i in range(self.iterations):

            w_t_1 = weights - self.beta * v
            
            gradient = _compute_gradient(X , y , w_t_1)

            v = self.beta * v - self.learning_rate * gradient

            weights += v

            loss = mse_loss(y , np.dot(X , weights))
            loss_history.append(loss)

            print_details(iterations= i , weights=weights , y=y , X=X)
            
        return weights , loss_history