from evaluators.base import Evaluator

class ExactMatchEvaluator(Evaluator):  
    def evaluate(self, expected_query, actual_query):
        return expected_query == actual_query