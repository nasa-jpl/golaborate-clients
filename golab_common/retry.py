"""Retry, even simpler-er for windows support."""
import logging
import time
from decorator import decorator


def retry(max_retries=2, interval=1):
    # simplified retry decorator, for better windows support

    # no use of select from stdlib, other features not used removed
    @decorator
    def wrapper(func, *args, **kwargs):
        result = None
        last_exception = None
        for n in range(max_retries):
            try:
                result = func(*args, **kwargs)
                last_exception = None
                break
            except Exception as e:
                last_exception = e
                logging.info(f'Exception {e} encountered during {func.__name__}, retrying ({n}/max_retries)')
                time.sleep(interval)

        if result is None and last_exception is not None:
            raise last_exception
        return result

    # end of wrapper, now back in 'retry' scopy
    return wrapper
