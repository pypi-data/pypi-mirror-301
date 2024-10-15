from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ollama import Client
import re

class SQLAgent:
    def __init__(
        self,
        llm_api_url: str,
        model: str,
        database_driver: str,
        database_username: str,
        database_password: str,
        database_host: str,
        database_port: str,
        database_name: str,
        debug: bool = False,
    ):
        self.debug = debug

        # LLM configurations
        self.llm_api_url = llm_api_url
        self.model = model

        self.llm = Client(host=llm_api_url)

        # Database configuration
        database_url = f"{database_driver}://{database_username}:{database_password}@{database_host}:{database_port}/{database_name}"
        self.engine = create_engine(database_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Create metadata and reflect it from the database
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

        if self.debug:
            print(f"Reflected Tables: {self.metadata.tables.keys()}")

    def run(self, user_request: str, tables: list = None, allowed_statements: list = None, max_retry: int = 3) -> str:
        # Default allowed statements
        if allowed_statements is None:
            allowed_statements = ["SELECT"]

        # Get database schema and build prompts
        database_schema = self.get_database_schema_markdown(tables)
        prompts = self.build_prompts(user_request=user_request, database_schema=database_schema)

        if self.debug:
            print(f"Prompts:\n{prompts}")

        # Query LLM
        retry = 0
        while retry < max_retry:
            try:
                response = self.llm.generate(
                    model=self.model,
                    system=prompts["system_prompt"],
                    prompt=prompts["prompt"],
                )

                if self.debug:
                    print(response)

                if "response" in response:
                    sql_query = self.extract_sql_query(response["response"])

                    # Check if query is allowed
                    if sql_query.split()[0].upper() not in allowed_statements:
                        if self.debug:
                            print(f"Disallowed statement: {sql_query.split()[0]}")
                        return None

                    # Validate SQL syntax using EXPLAIN
                    syntax_valid, error_message = self.validate_sql_syntax(sql_query)
                    if syntax_valid:
                        return sql_query
                    else:
                        if self.debug:
                            print(f"Syntax error in generated SQL: {error_message}")
                        # Optionally, modify the prompt to help LLM correct the query
                        prompts["prompt"] += f"\nThe previous query had a syntax error: {error_message}\nPlease provide a corrected SQL query."
                        retry += 1
                        continue
            except Exception as e:
                if self.debug:
                    print(f"Error: {e}, retrying...")
                else:
                    raise e
            retry += 1
        return None  # Return None if max retries exceeded

    def validate_sql_syntax(self, sql_query: str) -> (bool, str):
        # Use EXPLAIN to check the syntax of the SQL query
        try:
            explain_query = f"EXPLAIN {sql_query}"
            with self.engine.connect() as connection:
                connection.execute(text(explain_query))
            return True, ""
        except Exception as e:
            return False, str(e)

    def remove_leading_based_on_second_line(self, text: str) -> str:
        # Existing implementation
        # Split the text into lines
        lines = text.splitlines()

        if len(lines) < 2:
            return text.strip()  # If there's only one line, return the stripped version

        # Detect the leading spaces or tabs on the second line
        second_line = lines[1]
        leading_whitespace = ''
        for char in second_line:
            if char in (' ', '\t'):
                leading_whitespace += char
            else:
                break

        # Process each line starting from the second one
        stripped_lines = []
        for line in lines:
            if line.startswith(leading_whitespace):
                # Remove the detected leading whitespace from each line
                stripped_lines.append(line[len(leading_whitespace):])
            else:
                stripped_lines.append(line)

        # Join the lines back together and return the result
        return "\n".join(stripped_lines).strip()

    def build_prompts(self, user_request: str, database_schema: str) -> dict:
        system_prompt = """
        You are an assistant tasked with generating SQL queries. Follow these guidelines:
        - You will be provided with a database schema and required query details.
        - Generate valid SQL queries based on the structure and requirements.
        - Ensure correct syntax, table names, column names, and appropriate clauses (e.g., SELECT, WHERE, JOIN).
        - Do not include explanations or comments in the output, only the SQL query.
        """

        prompt_template = """
        Database Schema:
        {database_schema}

        User's Request:
        {user_request}
        """

        prompt = prompt_template.format(
            database_schema=str(database_schema).strip(),
            user_request=str(user_request).strip(),
        )

        # Clean up prompts
        system_prompt = self.remove_leading_based_on_second_line(system_prompt)
        prompt = self.remove_leading_based_on_second_line(prompt)

        if self.debug:
            print("System Prompt:")
            print(system_prompt)
            print("User Prompt:")
            print(prompt)

        return {
            "system_prompt": system_prompt,
            "prompt": prompt
        }

    def get_database_schema_markdown(self, tables: list = None) -> str:
        def get_column_details(column):
            # Clean up the type string by removing 'COLLATE'
            col_type = str(column.type)
            if "COLLATE" in col_type:
                col_type = col_type.split("COLLATE")[0].strip()  # Remove everything after 'COLLATE'

            return {
                'name': column.name,
                'type': col_type,  # Use the cleaned-up column type
                'primary_key': 'Yes' if column.primary_key else 'No',
                'foreign_keys': ', '.join([str(fk.target_fullname) for fk in column.foreign_keys]) if column.foreign_keys else '',
                'nullable': 'Yes' if column.nullable else 'No',
                'default': str(column.default.arg) if column.default is not None else '',
                'indexed': 'Yes' if column.index else 'No',
                'unique': 'Yes' if column.unique else 'No'
            }

        def format_as_markdown_table(table_name, columns):
            header = "| Column      | Type       | Primary Key | Foreign Key       | Nullable | Default  | Indexed | Unique |\n"
            divider = "|-------------|------------|-------------|-------------------|----------|----------|---------|--------|\n"
            rows = [
                f"| {col['name']}   | {col['type']}  | {col['primary_key']}       | {col['foreign_keys']} | {col['nullable']}     | {col['default']}   | {col['indexed']}   | {col['unique']} |"
                for col in columns
            ]
            return f"### {table_name}\n" + header + divider + "\n".join(rows) + "\n"

        if tables is None:
            # Get schema for all tables in the database
            schema_markdown = [format_as_markdown_table(table_name, [get_column_details(col) for col in table.columns]) for table_name, table in self.metadata.tables.items()]
        else:
            # Get schema only for the specified tables
            schema_markdown = [format_as_markdown_table(table_name, [get_column_details(col) for col in self.metadata.tables[table_name].columns]) for table_name in tables if table_name in self.metadata.tables]

        return "\n".join(schema_markdown)

    def extract_sql_query(self, llm_response: str) -> str:
        # Remove common code fences like ```sql or ``` and also extra backticks
        cleaned_response = re.sub(r'```(sql)?', '', llm_response)  # Remove ```sql or ``` (backticks)

        # Strip any leading/trailing whitespace or newlines
        cleaned_response = cleaned_response.strip()

        # Handle multiline queries: replace multiple newlines with a single space
        cleaned_response = re.sub(r'\s+', ' ', cleaned_response).strip()

        return cleaned_response
