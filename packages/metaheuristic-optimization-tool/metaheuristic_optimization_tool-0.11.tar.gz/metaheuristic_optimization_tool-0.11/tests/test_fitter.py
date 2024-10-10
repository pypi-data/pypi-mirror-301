import sys
from mot.core import Fitter
import numpy as np
import pytest

def test_init():
    obj = Fitter()
    assert obj.NF == 0

def test_add_function():
    obj = Fitter()
    obj.add_function('some_func')
    assert obj.NF == 1
