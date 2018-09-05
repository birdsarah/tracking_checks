import json
import pandas as pd
import requests


def save_disconnect_json(file_path='disconnect.json'):
    """Fetch and save the latest disconnect.json.

    Accepts optional file_path for where the json should be stored. Default is
    'disconnect.json' in current directory.
    """
    url = 'https://services.disconnect.me/disconnect.json'
    response = requests.get(url)
    assert response.ok, f'Could not get disconnect.json: {response.status_code} , {response.reason}'
    with open(file_path, 'w') as f:
        f.write(json.dumps(response.json()))


def get_disconnect_df(file_path='disconnect.json'):
    """Process the disconnect json into a dataframe.

    The index of the dataframe is a domain, and the column category is the
    disconnect.me category (one of: Advertising, Analytics,
    Content, Disconnect, and Social).

    Accepts optional file_path for where the json is located.
    """
    with open(file_path, 'r') as f:
        disconnect_json = json.loads(f.read())

    lookup = {}
    for category in disconnect_json['categories'].keys():
        for item in disconnect_json['categories'][category]:
            for name in item:
                for parent_domain in item[name]:
                    for child_domain in item[name][parent_domain]:
                        lookup[child_domain] = category
    df = pd.DataFrame.from_dict(lookup, orient='index').rename(columns={0: 'category'})
    return df
