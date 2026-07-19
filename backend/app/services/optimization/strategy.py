from abc import ABC, abstractmethod

class OptimizerStrategy(ABC):
    """
    Abstract strategy class for all SEO optimization algorithms.
    """
    
    @abstractmethod
    async def optimize(self, context: dict) -> dict:
        """
        Executes the optimization algorithm using the provided page context.
        Returns a dictionary containing the optimized parameters.
        """
        pass
