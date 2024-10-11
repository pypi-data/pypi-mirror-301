# sql_scan/where_extractor.py
from sql_scan.table_extractor import extract_table_name

def extract_where_condition(lines, bookmark):
    """
    Extracts WHERE clauses from SQL lines based on a starting bookmark.

    Parameters:
    lines (list): List of SQL lines.
    bookmark (int): The index from which to start searching for WHERE clauses.

    Returns:
    list: A list of extracted WHERE clauses.
    """
    # SQL keywords that indicate the start of new statements
    sql_keywords = {
        "SELECT", "FROM", "GROUP", "ORDER", "HAVING", "LIMIT", "JOIN", "INNER", "LEFT", "RIGHT", 
        "OUTER", "CROSS", "UNION", "EXCEPT", "INTERSECT", "WITH", "INSERT", "UPDATE", "DELETE",
        "CREATE", "DROP", "ALTER", "TRUNCATE", "MERGE", "GRANT", "REVOKE", "COMMIT", "ROLLBACK", 
        "BEGIN", "END"
    }
    
    prev_line = ""
    bookmark_breaker = bookmark
    
    for i, line in enumerate(lines[bookmark + 1:], start=bookmark + 1):
        current_line = line.strip()
        keyword, table_name = extract_table_name(current_line, prev_line)
        prev_line = current_line
        
        # Continue if the current line indicates a JOIN operation
        if keyword == "JOIN":
            continue

        if (table_name) and ( keyword in {"FROM","INTO","UPDATE","MERGE INTO"}):
            bookmark_breaker = i  # Set the bookmark to the current line index
            break


        if keyword is None and table_name is None:
            bookmark_breaker = i + 1

    where_clauses = []  # To store extracted WHERE clauses
    where_clause = []  # To build a single WHERE clause
    start_copying = False  # Flag to indicate when to start copying lines
    
    for line in lines[bookmark:bookmark_breaker]:
        stripped_line = line.strip().upper()
        
        # Check for the start of a WHERE clause
        if "WHERE" in stripped_line and not stripped_line.startswith(tuple(sql_keywords)):
            start_copying = True
            if where_clause:
                where_clauses.append(''.join(where_clause))
                where_clause = []

        # Copy lines until another SQL keyword or semicolon is encountered
        if start_copying:
            if not stripped_line or stripped_line.startswith(tuple(sql_keywords)) or stripped_line.startswith(")") or stripped_line.startswith(";") or stripped_line.startswith("("):
                start_copying = False
                if where_clause:
                    where_clauses.append(''.join(where_clause))
                    where_clause = []
            
            else:
                where_clause.append(line)

    if where_clause:  # In case the last WHERE clause was not appended
        where_clauses.append(''.join(where_clause))

    return where_clauses
