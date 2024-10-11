# sql_scan/file_writer.py

import os 
from sql_scan.formatter import format_file
from sql_scan.table_extractor import extract_table_name
from sql_scan.where_extractor import extract_where_condition

def extract_data(sql_file_name, save_formatted_file):
    """
    Extracts table names and WHERE conditions from a SQL file and writes the results to a file.
    """
    if sql_file_name.endswith(".sql"):
        sql_file_name = sql_file_name[:-4]

    format_file(sql_file_name)
    input_file = f'formatted_{sql_file_name}.sql'
    output_file = f'{sql_file_name}_report.txt'

    with open(input_file, 'r') as file:
        lines = file.readlines()

    table_names = []
    bookmark = -1
    prev_line = ""

    with open(output_file, 'w') as output:
        for i, line in enumerate(lines):
            current_line = line.strip()
            keyword, table_name = extract_table_name(current_line, prev_line)
            if table_name:
                print(f'TABLE NAME: {table_name}\n')
                output.write(f'TABLE NAME: {table_name}\n')
                output.write(f'TABLE TYPE: {keyword}\n')
                print(f'TABLE TYPE: {keyword}\n')

                where_clauses = extract_where_condition(lines, i)
                if where_clauses:
                    output.write(f'WHERE CONDITION: {"".join(where_clauses)}\n')
                    print(f'WHERE CONDITION: {"".join(where_clauses)}\n')
                else:
                    output.write("NO WHERE CONDITION FOUND\n")
                    print("NO WHERE CONDITION FOUND\n")

                output.write('-' * 40 + '\n')
                print('-' * 40 + '\n')
                table_names.append(table_name)
            prev_line = current_line

    if not save_formatted_file :
        os.remove(input_file)

