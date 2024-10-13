from .gradient_descent import GradientDescent
from .coordinate_descent import CoordinateDescent
from .stochastic_gradient_descent import StocasticGradientDescent
from .nesterov_accelerated_gradient_descent import NesterovAcceleratedGradientDescent
from .proximal_gradient_descent import ProximalGradientDescent
from .newtons_method import NewtonMethod

class OptimizerFactory:
    """
    Factory class to create optimizer instances.

    Methods:
        get_optimizer(optimizer_type, **kwargs): Returns an optimizer instance based on the type.
    """

    @staticmethod
    def get_optimizer(optimizer_type, learning_rate , iterations , tolerance , method , batch_size ):
        """
        Returns an optimizer instance based on the specified type.

        Args:
            optimizer_type (str): The type of optimizer to create.
            **kwargs: Additional arguments for the optimizer.

        Returns:
            Optimizier: An instance of the specified optimizer.
        """
        if optimizer_type == "gradient_descent" and method == "proximal":
            return ProximalGradientDescent(learning_rate=learning_rate , iterations= iterations , tolerance=tolerance)
        if optimizer_type == "gradient_descent":
            return GradientDescent(learning_rate= learning_rate , iterations= iterations, tolerance=tolerance)
        if optimizer_type == "coordinate_descent":
            return CoordinateDescent(learning_rate= learning_rate , iterations= iterations , method=method , tolerance=tolerance)
        if optimizer_type == "sgd":
            return StocasticGradientDescent(learning_rate=learning_rate , iterations=iterations , batch_size=batch_size ,tolerance=tolerance)
        if optimizer_type=="graduent_descent" and method=="nestrov":
            return NesterovAcceleratedGradientDescent(learning_rate=learning_rate , iterations=iterations , tolerance=tolerance)
        if optimizer_type=="newton":
            return NewtonMethod(iterations=iterations , tolerance=tolerance)
        