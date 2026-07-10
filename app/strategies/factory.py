from app.strategies.fifo import FIFOStrategy
from app.strategies.fefo import FEFOStrategy
from app.strategies.batch import BatchStrategy


class StrategyFactory:

    @staticmethod
    def get_strategy(strategy_name: str):

        if strategy_name == "FIFO":
            return FIFOStrategy()

        elif strategy_name == "FEFO":
            return FEFOStrategy()

        elif strategy_name == "BATCH":
            return BatchStrategy()

        raise ValueError("Invalid strategy")