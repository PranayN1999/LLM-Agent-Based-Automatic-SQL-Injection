from langchain.tools import tool
from automation_scripts.find_all_tables import find_all_tables

@tool
def find_table_names_tool() -> dict:
    """
    Finds all table names in the database using blind SQL injection.

    Returns:
        dict: A dictionary containing the list of table names or an error message.
    """
    try:
        table_names = find_all_tables()
        return {"table_names": table_names} if table_names else {"error": "No tables found in the database."}
    except ValueError as e:
        return {"error": str(e)}
