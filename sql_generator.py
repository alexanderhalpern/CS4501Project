class SQLGenerator:
    def __init__(self, llm, db_cursor):
        self.llm = llm
        self.db_cursor = db_cursor

    def get_table_structure(self, table_name):
        self.db_cursor.execute(f"PRAGMA table_info({table_name})")  # For SQLite
        columns = self.db_cursor.fetchall()

        table_structure = f"CREATE TABLE {table_name} (\n"
        table_structure += ",\n".join([f"    {col[1]} {col[2]}" for col in columns])
        table_structure += "\n);"

        self.db_cursor.execute(f"SELECT * FROM {table_name} LIMIT 10")
        rows = self.db_cursor.fetchall()
        headers = [description[0] for description in self.db_cursor.description]

        if rows:
            for row in rows:
                values = ", ".join(
                    [repr(value) if isinstance(value, str) else str(value) for value in row]
                )
                table_structure += f"\nINSERT INTO {table_name} ({', '.join(headers)}) VALUES ({values});"

        return table_structure

    def execute(self, query):
        self.db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.db_cursor.fetchall()
        table_structures = ""

        for table in tables:
            table_name = table[0]
            table_structures += self.get_table_structure(table_name) + "\n\n"

        res = self.llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f'''

                    Given the following table structure, respond to the user query by generating a SQL query.
                    Your response should only contain the text for the SQL query and nothing else.

                    If asked about where it occurred, use Location as opposed to LSOA.

                    TABLE STRUCTURES:
                    {table_structures}

                    QUERY:
                    {query}
                    '''
                },
            ]
        )

        sql_query = res.choices[0].message.content
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        try:
            self.db_cursor.execute(sql_query)
        except Exception as e:
            return [], sql_query

        actual = []
        for row in self.db_cursor.fetchall():
            actual.append(row)

        print(actual, sql_query)

        return actual, sql_query
