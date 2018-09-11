import os
import sqlite3
import pandas as pd
from pathlib import Path

PROFILE_ROOT = None
DBS = [
    'cookies',
    'storage',
    'content-prefs',
    'webappsstore',
    'places',
    'favicons',
    'permissions'
]


def set_profile_root(profile_location):
    global PROFILE_ROOT
    assert os.path.exists(profile_location), 'Path does not exist'
    if isinstance(profile_location, str):
        PROFILE_ROOT = Path(profile_location)
    else:
        PROFILE_ROOT = profile_location


def get_profile_dir_from_part(part):
    if PROFILE_ROOT is None:
        raise UnboundLocalError(
            "PROFILE_ROOT is not set. Please set with `set_profile_root`")
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


def get_cookie_table_for_profile(profile_dir, convert_timestamps=True):
    db = get_db(profile_dir, 'cookies')
    df = pd.read_sql('SELECT * FROM moz_cookies', db, index_col='id')
    if convert_timestamps:
        df['creationTime'] = pd.to_datetime(df.creationTime * 1_000)
        df['lastAccessed'] = pd.to_datetime(df.lastAccessed * 1_000)
        df['expiry'] = pd.to_datetime(df.expiry * 1_000_000_000)
    df = df.sort_values(by='creationTime').reset_index(drop=True)
    return df


def get_local_storage_for_profile(profile_dir):
    db = get_db(profile_dir, 'webappsstore')
    df = pd.read_sql('SELECT * FROM webappsstore2', db, index_col='id')
    return df


def get_places_table_for_profile(profile_dir):
    db = get_db(profile_dir, 'places')
    df = pd.read_sql('SELECT * FROM moz_places', db, index_col='id')
    return df


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
