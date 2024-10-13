import numpy as np
from .optimizer import Optimizier

class NewtonMethod(Optimizier):
    def __init__(self, learning_rate=None, iterations=None, tolerance=None) -> None:
        super().__init__(learning_rate, iterations, tolerance)

    def optimize(self , X , y , initial_weights = None):

        m , n = X.shape
        weights = initial_weights.copy()
        loss_history = []
        for i in range(self.iterations):
            grad = self.gradient(X , y , weights)
            hess = self.hessian(X , weights)

            weights -= np.dot(np.linalg.inv(hess) , grad)
            loss = self.loss_function(X , y , weights)
            loss_history.append(loss)
            # if (i+1)%1 == 0:
            #     print(f"Iteration : {i+1} , Loss : {loss}")
            print(f"Iteration : {i+1} , Loss : {loss}")
            if i > 0 and abs(loss_history[-1] - loss_history[-2])<self.tolerance:
                print(f"Converged after {i+1} iterations")


        return weights , loss_history

    
    def sigmoid(self , z):
        return 1 / (1 + np.exp(-z))

    def loss_function(self , X , y, weights):
        h = self.sigmoid(np.dot(X , weights))
        #print(h)
        print(h)
        return -np.sum(y * np.log(h) + (1-y)*np.log(1-h))
    
    def gradient(self, X , y , weights):
        h = self.sigmoid(np.dot(X , weights))
        return np.dot(X.T , (h - y))
    
    def hessian(self, X , weights):
        # print("X : ", X.shape)
        # print("weights :", weights.shape)
        h = self.sigmoid(np.dot(X , weights))
        # print("h ", h.shape)
        diag = h * (1-h)
        # print(diag.shape)
        W = np.diag(diag)
        return np.dot(np.dot(X.T , W) , X)