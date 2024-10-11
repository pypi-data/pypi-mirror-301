# sql_scan/__init__.py

"""
sql_scan - A package for extracting and formatting SQL table names and WHERE conditions.
"""

# Import the necessary functions or classes from your modules
from .table_extractor import extract_table_name
from .where_extractor import extract_where_condition
from .formatter import format_file
from .file_writer import extract_data
import argparse

__all__ = [
    "extract_table_name",
    "extract_where_condition",
    "format_file",
    "extract_data"
]

__version__ = "0.1.0"
__author__ = "Meghsham Jambhulkar"

def main():
    parser = argparse.ArgumentParser(description='Extract data from SQL files.')
    parser.add_argument('filename', type=str, help='The SQL file to process')
    parser.add_argument('--save', type=bool, default=True, 
                        help='Whether to save the formatted file (default: True)')

    args = parser.parse_args()

    # Call the extract_data function with the provided arguments
    extract_data(args.filename, args.save)

if __name__ == '__main__':
    main()
