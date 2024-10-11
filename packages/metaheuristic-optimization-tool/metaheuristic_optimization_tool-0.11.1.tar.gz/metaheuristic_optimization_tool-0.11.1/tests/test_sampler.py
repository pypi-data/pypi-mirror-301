import sys
from mot.core import Sampler
import numpy as np
import pytest



def test_init():
    obj = Sampler()
    assert len(obj.v_label) == 0


def test_add_one_variable():
    obj = Sampler()
    obj.add_variable('label', 0, 10,
                          unit='',
                          dist_fcn='uniform')
    assert len(obj.v_label) == 1


def test_add_two_variable():
    obj = Sampler()
    obj.clear()
    print(obj.v_label)
    obj.add_variable('label', 0, 10,
                     unit='',
                     dist_fcn='uniform')
    print(obj.v_label)

    obj.add_variable('label2', 0, 10,
                     unit='',
                     dist_fcn='uniform')
    print(obj.v_label)

    assert len(obj.v_label) == 2


def test_check_kwargs():
    obj = Sampler()
    obj.clear()
    obj.add_variable('label', 0, 10, unit='', 
                     dist_fcn='normal', **{'loc': 5, 'scale': 1})
    assert obj.v_fcn_args[-1] == {'loc':5, 'scale':1}

def test_wrong_kwarg_dist():
    obj = Sampler()
    obj.clear()
    try:
        obj.add_variable('label', 0, 10, unit='', dist_fcn='normal', **{'a': 1})
        assert False
    except ValueError:
        assert True

def test_random_range():
    obj = Sampler()
    obj.clear()
    obj.add_variable('label', 0, 10, unit='', dist_fcn='uniform')
    obj.add_variable('label2', 0, 10, unit='', dist_fcn='normal', **{'loc': 5, 'scale': 1})
    new = obj.random()
    b = True
    for i in new:
        if i > 10 or i < 0:
            b = False
    assert b


def test_random_fail():
    obj = Sampler()
    obj.clear()
    obj.add_variable('failure', 0, 10, unit='', dist_fcn='normal', **{'loc':300, 'scale': 1})
    try:
        obj.random()
        assert False
    except ValueError:
        assert True    


def test_is_it_in():
    obj = Sampler()
    obj.clear()

    obj.add_variable('label', 0, 10, unit='', dist_fcn='uniform')
    assert obj.is_it_in(5, 0)


def test_is_it_in_fail():
    obj = Sampler()
    obj.clear()

    obj.add_variable('label', 0, 10, unit='', dist_fcn='uniform')
    assert not obj.is_it_in(20, 0)












