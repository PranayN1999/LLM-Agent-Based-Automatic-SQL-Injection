from langchain.agents import tool
from automation_scripts.find_columns_for_table import find_columns_for_table
from config.settings import SESSION_COOKIE, SERVER_URL

@tool
def find_columns_for_table(table_name: str) -> str:
    """
    Finds all columns for a specific table.
    Args:
        table_name (str): The name of the table to inspect.
    Returns:
        str: Comma-separated column names.
    """
    columns = find_columns_for_table(SESSION_COOKIE, SERVER_URL, table_name)
    return ', '.join(columns) if columns else f"No columns found for table: {table_name}."
