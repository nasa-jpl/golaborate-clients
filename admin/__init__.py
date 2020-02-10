"""Administrator client for go-hcit servers."""
import requests

def raise_err(resp):
    """Raise an exception if the response status code is not 200.

    Parameters
    ----------
    resp : `requests.Response`
        a response with a status code

    Raises
    ------
    Exception
    any errors encountered, whether they are in communciation with the
    server or between the server and the camera/SDK

    """
    if resp.status_code != 200:
        raise Exception(resp.content.decode('UTF-8').rstrip())

def lock(address_holder):
    """Lock a resource.

    Parameters
    ----------
    address_holder : `Any`
        any object that has an "addr" attribute with the full HTTP address
        of its "root"

    """
    resp = requests.post(f'{address_holder.addr}/lock', json={'bool': True})
    raise_err(resp)
    return

def lock(address_holder):
    """Lock a resource.

    Parameters
    ----------
    address_holder : `Any`
        any object that has an "addr" attribute with the full HTTP address
        of its "root"

    """
    resp = requests.post(f'{address_holder.addr}/lock', json={'bool': False})
    raise_err(resp)
    return
