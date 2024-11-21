from sql_generator import SQLGenerator
from evaluators.llm_evaluator import LLMEvaluator
from evaluators.exact_match_evaluator import ExactMatchEvaluator
from evaluators.execution_evaluator import ExecutionEvaluator
import mysql.connector
from openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="password",
    database="SQLTests"
)

cursor = conn.cursor()


def test():
    llm = OpenAI()
    total_llm_tests = 0
    passed_llm_tests = 0

    total_exact_match_tests = 0
    passed_exact_match_tests = 0

    total_execution_tests = 0
    passed_execution_tests = 0

    tests = json.load(open("GreaterManchesterCrime.json"))

    llm_evaluator = LLMEvaluator(llm)
    exact_match_evaluator = ExactMatchEvaluator()
    execution_evaluator = ExecutionEvaluator()
    sql_generator = SQLGenerator(llm, cursor)


    # it is a giant list of dictionaries. i need to loop through query and question
    for test in tests:
        sql_query = test["query"]
        user_query = test["question"]

        expected = []
        try:
            cursor.execute(sql_query)
        except Exception as e:
            return [], sql_query

        for row in cursor.fetchall():
            expected.append(row)

        actual, actual_query = sql_generator.execute(user_query)

        llm_evaluation_result = llm_evaluator.evaluate(
            user_query, expected, actual, sql_query, actual_query)
        
        exact_match_result = exact_match_evaluator.evaluate(
            sql_query, actual_query)
        
        execution_result = execution_evaluator.evaluate(
            expected, actual)

        passed_llm_tests += llm_evaluation_result
        total_llm_tests += 1

        passed_exact_match_tests += exact_match_result
        total_exact_match_tests += 1

        passed_execution_tests += execution_result
        total_execution_tests += 1

        if llm_evaluation_result != execution_result:
            print(f"Query: {user_query}")
            print(f"Expected Results: {expected}")
            print(f"Actual Results: {actual}")
            print(f"Expected Query: {sql_query}")
            print(f"Actual Query: {actual_query}")
            print(f"LLM Evaluation: {llm_evaluation_result}")
            print(f"Execution Evaluation: {execution_result}")
            print("----------------------------------")


    print(f"LLM: {passed_llm_tests}/{total_llm_tests}")
    print(f"Exact Match: {passed_exact_match_tests}/{total_exact_match_tests}")
    print(f"Execution: {passed_execution_tests}/{total_execution_tests}")
    

if __name__ == "__main__":
    test()
