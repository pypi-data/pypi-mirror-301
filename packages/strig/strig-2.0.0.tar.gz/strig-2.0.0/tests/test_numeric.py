import sys, os
import pytest 
sys.path.append(os.getcwd())

from src.strig import numeric
import os


def test_default():
    generated = numeric()
    assert len(str(generated)) == 6

def test_prefix():
    generated = str(numeric(prefix=123))

    assert len(generated) == 9
    assert generated[:3] == "123"

    with pytest.raises(TypeError):
        numeric(prefix="abc")

    
def test_length():
    generated = numeric(200)
    assert len(str(generated)) == 200
