from sql_generator import SQLGenerator
from evaluators.llm_evaluator import LLMEvaluator
from evaluators.exact_match_evaluator import ExactMatchEvaluator
from evaluators.execution_evaluator import ExecutionEvaluator
import mysql.connector
from openai import OpenAI
import json
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

my_sql_conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Ajh020304",
    database="SQLTests"
)

def test():
    llm = OpenAI()

    llm_evaluator = LLMEvaluator(llm)
    exact_match_evaluator = ExactMatchEvaluator()
    execution_evaluator = ExecutionEvaluator()

    databases = os.listdir("./databases")
    databases.sort(key=lambda x: x.endswith(".sql"))
    databases = databases[1:]
    print(databases)

    for database in databases:
        tests_path = f"./examples/{database.split('.')[0]}.json"
        if not os.path.exists(tests_path):
            print(f"Test file not found for {database}. Skipping...")
            continue

        tests = json.load(open(tests_path))
        print(len(tests), database)

        total_llm_tests = 0
        passed_llm_tests = 0

        total_exact_match_tests = 0
        passed_exact_match_tests = 0

        total_execution_tests = 0
        passed_execution_tests = 0

        log_file = f"results_{database.split('.')[0]}.log"

        with open(log_file, "w") as log:
            log.write(f"Test Results for {database}\n")
            log.write("=" * 40 + "\n")

        if database.endswith(".sql"):
            cursor = my_sql_conn.cursor()
            sql_generator = SQLGenerator(llm, cursor)
        else:
            sqlite_conn = sqlite3.connect(f"./databases/{database}")
            cursor = sqlite_conn.cursor()
            sql_generator = SQLGenerator(llm, cursor)

        for test in tests:
            sql_query = test["query"]
            user_query = test["question"]

            expected = []
            try:
                cursor.execute(sql_query)
                for row in cursor.fetchall():
                    expected.append(row)
            except Exception as e:
                with open(log_file, "a") as log:
                    log.write(f"Error executing SQL query: {sql_query}\n")
                    log.write(f"Error: {str(e)}\n")
                continue

            actual, actual_query = sql_generator.execute(user_query)

            llm_evaluation_result = llm_evaluator.evaluate_with_queries(
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

            with open(log_file, "a") as log:
                log.write(f"User Query: {user_query}\n")
                log.write(f"SQL Query: {sql_query}\n")
                log.write(f"Actual Query: {actual_query}\n")
                log.write(f"Expected Results: {expected}\n")
                log.write(f"Actual Results: {actual}\n")
                log.write(f"LLM Evaluation: {llm_evaluation_result}\n")
                log.write(f"Exact Match Evaluation: {exact_match_result}\n")
                log.write(f"Execution Evaluation: {execution_result}\n")
                log.write("-" * 40 + "\n")

        with open(log_file, "a") as log:
            log.write(f"Final Results for {database}\n")
            log.write(f"LLM: {passed_llm_tests}/{total_llm_tests}\n")
            log.write(f"Exact Match: {passed_exact_match_tests}/{total_exact_match_tests}\n")
            log.write(f"Execution: {passed_execution_tests}/{total_execution_tests}\n")
            log.write("=" * 40 + "\n")

        print(f"LLM: {passed_llm_tests}/{total_llm_tests}")
        print(f"Exact Match: {passed_exact_match_tests}/{total_exact_match_tests}")
        print(f"Execution: {passed_execution_tests}/{total_execution_tests}")

        if not database.endswith(".sql"):
            sqlite_conn.close()
    

if __name__ == "__main__":
    test()
