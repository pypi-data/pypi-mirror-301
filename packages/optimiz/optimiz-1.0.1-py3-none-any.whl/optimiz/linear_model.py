import numpy as np
from .gradient_descent import GradientDescent
from .preprocessing import Preprocessing
from .optimizer_factory import OptimizerFactory
from .losses import mse_loss

class LinearModel:
    """
    Linear Regression model using various optimization algorithms.

    Args:
        learning_rate (float): The step size for weight updates.
        iterations (int): The number of iterations to perform.
        tolerance (float): The tolerance for stopping criteria.
        optimizer_type (str): The type of optimizer to use.
    """

    def __init__(self, learning_rate=0.01, iterations=1000, tolerance=1e-6, optimizer_type=None , method = None , batch_size=1) -> None:
        """
        Initializes the LinearRegression model.

        Args:
            learning_rate (float): The step size for weight updates.
            iterations (int): The number of iterations to perform.
            tolerance (float): The tolerance for stopping criteria.
            optimizer_type (str): The type of optimizer to use.
        """
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.tolerance = tolerance
        self.weights = None
        self.optimizer_type = optimizer_type
        # self.method = method
        if optimizer_type is None:
            raise ValueError("optimizer_type is None!")
        self.optimizer = OptimizerFactory.get_optimizer(
            optimizer_type=optimizer_type,
            learning_rate=learning_rate,
            iterations=iterations,
            tolerance=tolerance,
            method = method,
            batch_size = batch_size
        )
        self.batch_size = batch_size
        self.preprocessing = Preprocessing()

    def fit(self, X, y, scale=False):
        """
        Fits the Linear Regression model to the training data.

        Args:
            X (numpy.ndarray): The input feature matrix.
            y (numpy.ndarray): The target values.
            scale (bool): Whether to scale the features.

        Returns:
            None
        """
        X_with_bias = np.c_[np.ones((X.shape[0], 1)), X]
        if scale:
            X = self.preprocessing.scale(X)
        initial_weights = np.zeros(X_with_bias.shape[1])
        
        self.weights , loss_history = self.optimizer.optimize(X_with_bias, y, initial_weights)
        return loss_history

    def predict(self, X):
        """
        Predicts target values for the given input features.

        Args:
            X (numpy.ndarray): The input feature matrix.

        Returns:
            numpy.ndarray: The predicted target values.
        """
        if self.weights is None:
            raise ValueError("Model has not been trained. Call fit() first.")
        X_with_bias = np.c_[np.ones((X.shape[0], 1)), X]
        return X_with_bias.dot(self.weights)

    def mse_score(self, X, y):
        """
        Computes the Mean Squared Error (MSE) of the model predictions.

        Args:
            X (numpy.ndarray): The input feature matrix.
            y (numpy.ndarray): The target values.

        Returns:
            float: The computed MSE.
        """
        y_pred = self.predict(X)
        mse = mse_loss(y_true=y, y_pred=y_pred)
        return mse
    
