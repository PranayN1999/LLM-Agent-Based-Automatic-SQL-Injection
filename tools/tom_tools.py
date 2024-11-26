from langchain.agents import tool
from automation_scripts.find_tom_user_details import extract_tom_details
from config.settings import SESSION_COOKIE, SERVER_URL

@tool
def find_tom_details(table_name: str, columns: str) -> str:
    """
    Extracts details for the user 'Tom' from a specific table.
    Args:
        table_name (str): The name of the table to query.
        columns (str): Comma-separated column names in the table.
    Returns:
        str: Tom's details as a formatted string.
    """
    column_list = columns.split(', ')
    tom_details = extract_tom_details(SESSION_COOKIE, SERVER_URL, table_name, column_list)
    return str(tom_details) if tom_details else f"No details found for 'Tom' in table: {table_name}."
