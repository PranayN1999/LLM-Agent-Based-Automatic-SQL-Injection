from langchain.tools import tool
from automation_scripts.find_tom_user_details import extract_tom_details

@tool
def find_tom_details_tool(table_name: str, columns: list) -> dict:
    """
    Extracts details for the user 'Tom' from a specific table.

    Args:
        table_name (str): The name of the table to query.
        columns (list): A list of column names in the table.

    Returns:
        dict: A dictionary with column names as keys and extracted values or an error message.
    """
    try:
        print("Invoking find_tom_tool")
        tom_details = extract_tom_details(table_name, columns)
        return {"tom_details": tom_details} if tom_details else {"error": f"No details found for user 'Tom' in table {table_name}."}
    except ValueError as e:
        return {"error": str(e)}
