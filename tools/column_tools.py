from langchain.tools import tool
from automation_scripts.find_columns_for_table import find_columns_for_table

@tool
def find_columns_for_table_tool(table_name: str) -> dict:
    """
    Finds all column names for a specific table.

    Args:
        table_name (str): The name of the table to inspect.

    Returns:
        dict: A dictionary containing the list of column names or an error message.
    """
    try:
        print("Invoking columns tool")
        columns = find_columns_for_table(table_name)
        return {"columns": columns} if columns else {"error": f"No columns found for table {table_name}."}
    except ValueError as e:
        return {"error": str(e)}
