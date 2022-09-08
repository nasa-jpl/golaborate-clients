"""Common functions and macros."""
from .retry import DoNotRepeat


def raise_err(resp):
    """Raise an exception if the response status code is not 200.

    Parameters
    ----------
    resp : requests.Response
        a response with a status code

    Raises
    ------
    Exception
    any errors encountered, whether they are in communciation with the
    server or between the server and the camera/SDK

    """
    if resp.status_code == 404:
        raise DoNotRepeat('the called function was not supported by the server or hardware')
    if resp.status_code != 200:
        raise Exception(resp.text)


def niceaddr(addr):
    """ensure addr begins with http://"""
    if not addr.startswith('http://'):
        addr = 'http://' + addr

    if 'https' in addr:
        addr = addr.replace('https', 'http')

    return addr
