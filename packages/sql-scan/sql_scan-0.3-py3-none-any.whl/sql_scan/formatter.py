# sql_scan/formatter.py

import sqlparse

def format_file(file_name):
    """
    Reads and formats an SQL file using sqlparse.
    """
    if file_name.endswith(".sql"):
        file_name = file_name[:-4]

    with open(f'{file_name}.sql', 'r') as file:
        sql_content = file.read()

    sql_statements = sqlparse.split(sql_content)
    formatted_statements = [sqlparse.format(statement, reindent_aligned=True, keyword_case='upper',strip_comments= True) for statement in sql_statements]

    with open(f'formatted_{file_name}.sql', 'w') as file:
        file.write("\n\n".join(formatted_statements))
