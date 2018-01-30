""" Google Cloud Storage support for remote file interactivity """
from io import BytesIO
from pandas import compat
try:
    from google.cloud.storage import Client
except:
    raise ImportError("The google-cloud-storage library is required to "
                      "read gs:// files")

if compat.PY3:
    from urllib.parse import urlparse as parse_url
else:
    from urlparse import urlparse as parse_url


def _get_bucket_name(url):
    """Returns the bucket name from the gs:// url"""
    result = parse_url(url)
    return result.netloc


def _get_object_path(url):
    """Returns the object path from the gs:// url"""
    result = parse_url(url)
    return result.path.lstrip('/')


def get_filepath_or_buffer(filepath_or_buffer, encoding=None,
                           compression=None, mode=None):

    if mode is None:
        mode = 'rb'

    client = Client()
    bucket = client.get_bucket(_get_bucket_name(filepath_or_buffer))
    blob = bucket.blob(_get_object_path(filepath_or_buffer))
    data = BytesIO()
    blob.download_to_file(data)
    data.seek(0)
    filepath_or_buffer = data

    return filepath_or_buffer, None, compression
