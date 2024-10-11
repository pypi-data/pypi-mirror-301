import sys
from mot.core import Perturber
import numpy as np
import pytest



def test_init():
    obj = Perturber()
    assert len(obj.v_label) == 0


def test_add_one_variable():
    obj = Perturber()
    obj.add_variable('label', 0, 10,
                     unit='')
    assert len(obj.v_label) == 1


def test_add_two_variable():
    obj = Perturber()
    obj.add_variable('label', 0, 10,
                     unit='')
    obj.add_variable('label', 0, 10,
                     unit='')
    assert len(obj.v_label) == 2


def test_random_range():
    obj = Perturber()
    obj.add_variable('label', 0, 10, unit='')
    obj.add_variable('label2', 30, 100)
    b = True
    for i in range(100):
        new = obj.random()
        if new[0] > 10 or new[0] < 0:
            b = False
        if new[1] > 100 or new[1] < 30:
            b = False
    assert b

