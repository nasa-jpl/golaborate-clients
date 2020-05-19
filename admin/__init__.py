"""Administrator client for go-hcit servers."""
import requests

from golab_common import raise_err


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


def unlock(address_holder):
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
