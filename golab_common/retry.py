"""Retry, even simpler-er for windows support."""
import logging
import time
from functools import wraps


class DoNotRepeat(Exception):
    pass


def retry(max_retries=2, interval=1):
    # simplified retry decorator, for better windows support

    # no use of select from stdlib, other features not used removed
    def decorator(func):
        @wraps(func)
        def wrapper(func, *args, **kwargs):
            result = None
            last_exception = None
            for n in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                    last_exception = None
                    break
                except DoNotRepeat as e:
                    funcname = func.__name__
                    obj = getattr(func, '__self__', None)
                    if obj is not None:
                        # method, write it out nicely
                        clsname = obj.__self__.__class__.__name__
                        msg_front = f'{clsname}.{funcname}'
                    else:
                        msg_front = f'{funcname}'
                    raise ValueError(f'{msg_front} was not supported by the server or hardware')
                except Exception as e:
                    last_exception = e
                    logging.info(f'Exception {e} encountered during {func.__name__}, retrying ({n}/max_retries)')
                    time.sleep(interval)

            if result is None and last_exception is not None:
                raise last_exception
            return result
        return wrapper
    return decorator
