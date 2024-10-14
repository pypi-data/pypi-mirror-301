import sys, os
sys.path.append(os.getcwd())

from src.strig import alpha
from utils import has_upper, has_lower
import os


def test_default():
    generated = alpha()
    assert len(generated) == 6

    ## As the generated value is random, it does not always
    ## include numbers. With this absurdly long string 
    ## the chance for there to be a upper and lower case
    ## is almost guaranteed
    generated_long = alpha(10000)
    assert has_upper(generated_long) == True
    assert has_lower(generated_long) == True

def test_uppercase():
    generated = alpha(case="upper")
    assert has_upper(generated) == True
    assert has_lower(generated) == False

def test_lowercase():
    generated = alpha(case="lower")
    assert has_upper(generated) == False
    assert has_lower(generated) == True

def test_prefix():
    generated = alpha(prefix="abc")
    assert len(generated) == 9
    assert generated[:3] == "abc"
    
def test_length():
    generated = alpha(200)
    assert len(generated) == 200
