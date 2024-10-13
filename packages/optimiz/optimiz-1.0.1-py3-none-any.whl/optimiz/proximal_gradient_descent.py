"""Proximal Gradient Descent is desgined to for solving problem that have a nonsmooth or composite objective function.
Example - mse + L1 
mse is smooth (differentiable ) , L1(Lassos) is nonsmooth
"""
from .optimizer import Optimizier
from .utils import _compute_gradient
from .utils import print_details
import numpy as np
from .utils import mse_loss

class ProximalGradientDescent(Optimizier):

    def __init__(self, learning_rate=None, iterations=None, tolerance=None , lambda_=0.01) -> None:
        super().__init__(learning_rate, iterations, tolerance)
        self.lambda_ = 0.01

    def optimize(self , X , y , initial_weights):
        weights = initial_weights.copy()
        loss_history = []
        for i in range(self.iterations):
            gradient = _compute_gradient(X , y , weights)
            z_t_1 = weights - self.learning_rate * gradient

            weights = self.soft_tresholding(z_t_1, self.learning_rate , self.lambda_)
            loss = mse_loss(y , X.dot(weights))
            loss_history.append(loss)
            print_details(i , weights=weights , y=y , X=X)
        return weights , loss_history
    
    def soft_tresholding(self , z_t_1 , learning_rate , lambda_):
        return np.sign(z_t_1) * np.maximum(np.abs(z_t_1) - learning_rate * lambda_ , 0)
    