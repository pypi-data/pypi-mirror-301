import sys, os
sys.path.append(os.getcwd())

from src.strig import alphanumeric
from utils import has_upper, has_lower, has_number
import os


def test_default():
    generated = alphanumeric()
    assert len(generated) == 6

    ## As the generated value is random, it does not always
    ## include numbers. With this absurdly long string 
    ## the chance for there to be a number, upper and lower case
    ## is almost guaranteed
    generated_long = alphanumeric(10000)
    assert has_number(generated_long) == True
    assert has_upper(generated_long) == True
    assert has_lower(generated_long) == True

def test_uppercase():
    generated = alphanumeric(case="upper")
    assert has_upper(generated) == True
    assert has_lower(generated) == False

def test_lowercase():
    generated = alphanumeric(case="lower")
    assert has_upper(generated) == False
    assert has_lower(generated) == True

def test_prefix():
    generated = alphanumeric(prefix="abc")
    assert len(generated) == 9
    assert generated[:3] == "abc"
    
def test_length():
    generated = alphanumeric(200)
    assert len(generated) == 200
