"""This module contains the secret manager for the unicloud package."""
import base64
import json


def encode(secret_file: str, path: bool = True) -> bytes:
    """encode.

        encode the secret file to base64 string to be used in the environment variable

    Parameters
    ----------
    secret_file: [str]
        the path to the service account file
    path: [bool]
        True if the scret_file is a path or False if it is a string content of the secret file

    Returns
    -------
    byte string
    """
    if path:
        content = json.load(open(secret_file))
    else:
        content = secret_file

    dumped_service_account = json.dumps(content)
    encoded_service_account = base64.b64encode(dumped_service_account.encode())
    return encoded_service_account


def decode(string: str) -> str:
    """decode.

        decode the base64 string to the original secret file content

    Parameters
    ----------
    string: [bytes]
        the content of the secret file encoded with base64

    Returns
    -------
    str:
        google cloud service account content
    """
    service_key = json.loads(base64.b64decode(string).decode())
    return service_key
