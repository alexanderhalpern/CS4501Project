from evaluators.base import Evaluator

class ExecutionEvaluator(Evaluator):
    def evaluate(self, expected_results, actual_results):
        if not expected_results or not actual_results:
            return len(expected_results) == len(actual_results)

        expected_tuple = expected_results[0]
        actual_tuple = actual_results[0]

        if isinstance(expected_tuple, tuple) and isinstance(actual_tuple, tuple):
            return all(item in actual_tuple for item in expected_tuple) or \
                   all(item in expected_tuple for item in actual_tuple) or \
                   expected_tuple == actual_tuple

        return expected_tuple in actual_tuple or actual_tuple in expected_tuple or expected_tuple == actual_tuple
