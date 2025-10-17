import os

import boto3

_session = boto3.Session()
ssm = _session.resource('ssm')

def get_secret(key: str) -> str:
    if value := os.environ.get(key):
        return value

    return ssm.get_parameter(Name=key)
