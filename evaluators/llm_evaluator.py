from evaluators.base import Evaluator

class LLMEvaluator (Evaluator):
    def __init__(self, llm):
        self.llm = llm

    def evaluate(self, query, expected, actual, expected_query, actual_query):
        # Evaluate the query
        res = self.llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f'''
                    Evaluate whether the ACTUAL results are sufficient based on the EXPECTED results and the query that the user wrote.
                    Respond with only TRUE or FALSE.
                    
                    QUERY:
                    {query}
                    
                    EXPECTED:
                    {expected}
                    
                    ACTUAL:
                    {actual}
                    '''
                },
            ]
        )

        evaluation = res.choices[0].message.content == "TRUE"

        # if evaluation == False:
        #     print(f"Query: {query}")
        #     print(f"Expected Results: {expected}")
        #     print(f"Actual Results: {actual}")
        #     print(f"Expected Query: {expected_query}")
        #     print(f"Actual Query: {actual_query}")
        #     print(f"Evaluation: {evaluation}")
        #     print("----------------------------------")

        return evaluation

    def evaluate_with_queries(self, query, expected, actual, expected_query, actual_query):
        # Evaluate the query
        res = self.llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f'''
                    Evaluate whether both groups of queries and results correctly answer the user query. 
                    Bias true instead of false if unsure.
                    Respond with TRUE if both groups are correct, and FALSE any of the groups is incorrect.
                    
                    QUERY:
                    {query}
                    
                    QUERY 1 AND RESULTS:
                    {expected_query}
                    {expected}
                    
                    QUERY 2 AND RESULTS:
                    {actual_query}
                    {actual}
                    '''
                },
            ]
        )

        evaluation = res.choices[0].message.content == "TRUE"

        # if evaluation == False:
        #     print(f"Query: {query}")
        #     print(f"Expected Results: {expected}")
        #     print(f"Actual Results: {actual}")
        #     print(f"Expected Query: {expected_query}")
        #     print(f"Actual Query: {actual_query}")
        #     print(f"Evaluation: {evaluation}")
        #     print("----------------------------------")

        return evaluation
