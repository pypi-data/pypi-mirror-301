import os
import sys

sys.path.append(os.getcwd())

import os

from utils import has_lower, has_number, has_upper, has_urlsafe

from src.strig import urlsafe


def test_default():
    generated = urlsafe()
    assert len(generated) == 6
    assert has_urlsafe(generated) == True

    ## As the generated value is random, it does not always
    ## include numbers. With this absurdly long string
    ## the chance for there to be a number, upper and lower case
    ## is almost guaranteed
    generated_long = urlsafe(10000)
    assert has_number(generated_long) == True
    assert has_upper(generated_long) == True
    assert has_lower(generated_long) == True


def test_prefix():
    generated = urlsafe(prefix="abc")
    assert len(generated) == 9
    assert generated[:3] == "abc"


def test_length():
    generated = urlsafe(200)
    assert len(generated) == 200
