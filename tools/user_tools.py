from langchain.tools import tool
from automation_scripts.find_all_users import find_users

@tool
def find_users_in_table_tool(table_name: str, userid_column: str) -> dict:
    """
    Extracts user IDs from a specific table and column.

    Args:
        table_name (str): The name of the table to query.
        userid_column (str): The column holding user IDs.

    Returns:
        dict: A dictionary containing the list of user IDs or an error message.
    """
    try:
        users = find_users(table_name, userid_column)
        return {"user_ids": users} if users else {"error": f"No users found in column {userid_column} of table {table_name}."}
    except ValueError as e:
        return {"error": str(e)}
