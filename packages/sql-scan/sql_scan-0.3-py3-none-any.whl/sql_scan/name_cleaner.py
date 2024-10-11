# sql_scan/name_cleaner.py

import re

def name_cleaner(name):
    """
    Cleans up table names by removing unwanted characters and ensuring valid characters.
    """
    cleaned_name = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', name)
    cleaned_name = re.sub(r'[^\w\-]', '', cleaned_name)
    return cleaned_name
