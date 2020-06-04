"""Tests the animals.py file in the biosim folder."""

from biosim.animals import Animals
import pytest


@pytest.fixture
def test_set_parameters(request):
    Animals.set_parameters(request.param)
    yield
    Animals.set_parameters(Animals.params)

def test_age():
    a = Animals()
    for n in range(10):
        a.age_increase()
        assert a.age_increase() == n + 1


def test_init():
    
    herb = Herbivore(5, 40)

    assert herb.age == 5
    assert herb.weight == 40

#def test_Herbivore_issubclass():
