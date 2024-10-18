from sql_generator import SQLGenerator
from llm_evaluator import LLMEvaluator
import mysql.connector
from openai import OpenAI
import json

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Password1!",
    database="cs4501"
)

cursor = conn.cursor()


def test():
    llm = OpenAI()
    total_tests = 0
    passed_tests = 0

    tests = json.load(open("GreaterManchesterCrime.json"))
    llm_evaluator = LLMEvaluator(llm)
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

        passed_tests += llm_evaluator.evaluate(
            user_query, expected, actual, sql_query, actual_query)
        total_tests += 1

    return passed_tests, total_tests


if __name__ == "__main__":
    print(test())
