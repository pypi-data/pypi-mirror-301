import numpy as np

class Preprocessing:
    """
    Class for preprocessing data, including scaling.

    Attributes:
        mean (numpy.ndarray): The mean of the features.
        std (numpy.ndarray): The standard deviation of the features.
    """

    def __init__(self) -> None:
        """
        Initializes the Preprocessing class.
        """
        self.mean = None
        self.std = None

    def scale(self, X):
        """
        Scales the features to have zero mean and unit variance.

        Args:
            X (numpy.ndarray): The input feature matrix.

        Returns:
            numpy.ndarray: The scaled feature matrix.
        """
        self.mean = np.mean(X, axis=0)
        self.std = np.std(X, axis=0)
        return (X - self.mean) / self.std