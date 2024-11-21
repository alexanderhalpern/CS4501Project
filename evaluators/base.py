from abc import ABC, abstractmethod


class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, expected_query, actual_query):
        pass