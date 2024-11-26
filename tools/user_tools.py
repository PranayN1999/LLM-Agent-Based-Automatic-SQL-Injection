from langchain.agents import tool
from automation_scripts.find_all_users import find_users
from config.settings import SESSION_COOKIE, SERVER_URL

@tool
def find_users_in_table(table_name: str, userid_column: str) -> str:
    """
    Extracts all user IDs from a specific table and column.
    Args:
        table_name (str): The name of the table to query.
        userid_column (str): The column holding user IDs.
    Returns:
        str: Comma-separated user IDs.
    """
    users = find_users(SESSION_COOKIE, SERVER_URL, table_name, userid_column)
    return ', '.join(users) if users else f"No users found in table: {table_name}."
