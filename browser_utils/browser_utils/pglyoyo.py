import json
import pandas as pd
import requests
import tldextract


def save_pgl(file_path='pgl.txt'):
    """Fetch and save latest pgl file

    Credit: Peter Lowe - pgl@yoyo.org - https://pgl.yoyo.org/ - https://twitter.com/pgl

    Accepts optional file_path for where the txt should be stored. Default is
    'pgl.txt' in current directory.
    """
    url = 'https://pgl.yoyo.org/as/serverlist.php?hostformat=nohtml&showintro=0'
    response = requests.get(url)
    assert response.ok, f'Could not get pgl files: {response.status_code} , {response.reason}'
    with open(file_path, 'w') as f:
        f.write(response.text)


def get_pgl_df(file_path='pgl.txt'):
    """Process the pgl file into a pandas dataframe.

    Accepts optional file_path for where the json is located.
    """
    def get_base_domain(item):
        extract = tldextract.extract(item)
        return f'{extract.domain}.{extract.suffix}'
    df = pd.read_csv(file_path, names=['domain'])
    df['baseDomain'] = df.domain.apply(get_base_domain)
    return df

