from golab_common.retry import retry

import pytest


CNTR1 = 0
STOP_FAIL_AT1 = 2

CNTR2 = 0
STOP_FAIL_AT2 = 2

error_text = 'not enough iterations'


@retry(max_retries=3, interval=0.001)
def flaky_function_that_will_pass():
    global CNTR1
    print(CNTR1)
    if CNTR1 < STOP_FAIL_AT1:
        CNTR1 += 1
        raise StopIteration(error_text)

    return


@retry(max_retries=1, interval=0.001)
def flaky_function_that_will_fail():
    global CNTR2
    if CNTR2 < STOP_FAIL_AT2:
        CNTR2 += 1
        raise StopIteration(error_text)

    return


def test_retry_ameliorates_flaky_behavior():
    flaky_function_that_will_pass()


def test_retry_fails_not_enough_iter():
    with pytest.raises(StopIteration, match=error_text):
        flaky_function_that_will_fail()
