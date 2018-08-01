import os
import sqlite3

import pandas as pd

PROFILE_ROOT = '/home/bird/.mozilla/firefox/'
DBS = [
    'cookies',
    'storage',
    'content-prefs',
    'webappsstore',
    'places',
    'favicons',
    'permissions'
]


def get_profile_dir_from_part(part):
    candidates = [
        os.path.join(PROFILE_ROOT, x)
        for x in os.listdir(PROFILE_ROOT) if part in x
    ]
    if len(candidates) == 0:
        raise KeyError("Not available")
    if len(candidates) == 1:
        return candidates[0]
    else:
        return candidates


def get_cookie_table_for_profile(profile_dir):
    db = get_db(profile_dir, 'cookies')
    return pd.read_sql('SELECT * FROM moz_cookies', db)


def get_local_storage_for_profile(profile_dir):
    db = get_db(profile_dir, 'webappsstore')
    return pd.read_sql('SELECT * FROM webappsstore2', db)


def get_db(profile_dir, db_name):
    assert db_name in DBS
    db_file = os.path.join(profile_dir, f'{db_name}.sqlite')
    return sqlite3.connect(db_file)


def list_tables_in_db(db):
    print(
        db.cursor().execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        ).fetchall()
    )
