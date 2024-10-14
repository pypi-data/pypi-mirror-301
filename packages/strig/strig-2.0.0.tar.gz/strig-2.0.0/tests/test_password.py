import os
import sys

sys.path.append(os.getcwd())

import os

from utils import has_lower, has_number, has_symbol, has_upper

from src.strig import password


def test_default():
    generated = password()
    assert len(generated) == 20
    assert has_number(generated) == True
    assert has_symbol(generated) == True

    ## As the generated value is random, it does not always
    ## include numbers. With this absurdly long string
    ## the chance for there to be a number, upper and lower case
    ## is almost guaranteed
    generated_long = password(10000)
    assert has_upper(generated_long) == True
    assert has_lower(generated_long) == True


def test_uppercase():
    generated = password(case="upper")
    assert has_upper(generated) == True
    assert has_lower(generated) == False


def test_lowercase():
    generated = password(case="lower")
    assert has_upper(generated) == False
    assert has_lower(generated) == True


def test_digits():
    generated = password()
    assert has_number(generated) == True
    no_d_generated = password(digits=False)
    assert has_number(no_d_generated) == False


def test_symbols():
    generated = password()
    assert has_symbol(generated) == True
    no_s_generated = password(symbols=False)
    assert has_symbol(no_s_generated) == False


def test_prefix():
    generated = password(prefix="abc")
    assert len(generated) == 23
    assert generated[:3] == "abc"


def test_length():
    generated = password(200)
    assert len(generated) == 200
