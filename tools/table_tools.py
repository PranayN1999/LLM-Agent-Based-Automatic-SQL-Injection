from langchain.agents import tool
from automation_scripts.find_all_tables import find_all_tables
from config.settings import SESSION_COOKIE, SERVER_URL

@tool
def find_table_names() -> str:
    """
    Finds all table names in the database using blind SQL injection.
    Returns:
        str: Comma-separated table names.
    """
    table_names = find_all_tables(SESSION_COOKIE, SERVER_URL)
    return ', '.join(table_names) if table_names else "No tables found."
