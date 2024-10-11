# sql_scan/table_extractor.py

import re
from sql_scan.name_cleaner import name_cleaner

def extract_table_name(current_line, prev_line):
    """
    Extracts potential table names from SQL lines based on previous context.
    """
    tokens = {"SELECT", "FROM", "JOIN", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP"}
    patterns = {
    "FROM": r'\bFROM\s+([a-zA-Z0-9_\.]+)',  # Table names after FROM clause
    "JOIN": r'\bJOIN\s+([a-zA-Z0-9_\.]+)',  # Table names after JOIN clause
    "WITH": r'\bWITH\s+([a-zA-Z0-9_\.]+)',  # Table names after WITH clause (CTE)
    "INSERT INTO": r'\bINSERT\s+INTO\s+([a-zA-Z0-9_\.]+)',  # Table name after INSERT INTO clause
    "UPDATE": r'\bUPDATE\s+([a-zA-Z0-9_\.]+)',  # Table name after UPDATE clause
    "DELETE FROM": r'\bDELETE\s+FROM\s+([a-zA-Z0-9_\.]+)',  # Table name after DELETE FROM clause
    "MERGE INTO": r'\bMERGE\s+INTO\s+([a-zA-Z0-9_\.]+)',  # Table name after MERGE INTO clause
    "CREATE TABLE": r'\bCREATE\s+TABLE\s+([a-zA-Z0-9_\.]+)',  # Table name after CREATE TABLE
    "ALTER TABLE": r'\bALTER\s+TABLE\s+([a-zA-Z0-9_\.]+)',  # Table name after ALTER TABLE
    "DROP TABLE": r'\bDROP\s+TABLE\s+([a-zA-Z0-9_\.]+)',  # Table name after DROP TABLE
    "TRUNCATE TABLE": r'\bTRUNCATE\s+TABLE\s+([a-zA-Z0-9_\.]+)',  # Table name after TRUNCATE TABLE
    "RENAME TABLE": r'\bRENAME\s+TABLE\s+([a-zA-Z0-9_\.]+)',  # Table name after RENAME TABLE
    "COPY INTO": r'\bCOPY\s+INTO\s+([a-zA-Z0-9_\.]+)'  # Specific to databases like Snowflake
    }
    
    current_line = current_line.strip().strip(';,')
    prev_line = prev_line.strip().strip(';,')
    
    if "FROM" in prev_line.upper() and len(prev_line) == len("FROM"):
        table_name = current_line.split()[0]
        clean_name = name_cleaner(table_name)
        if clean_name.upper() not in tokens:
            return "FROM", clean_name

    for keyword, pattern in patterns.items():
        match = re.search(pattern, current_line, re.IGNORECASE)
        if match:
            clean_name = name_cleaner(match.group(1))
            if clean_name.split()[0].upper() not in tokens:
                return keyword, clean_name

    return None, None
