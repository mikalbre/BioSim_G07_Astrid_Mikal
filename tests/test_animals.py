"""Tests the animals.py file in the biosim folder."""

from biosim import animals
import pytest


@pytest.fixture
def set_parameters(request):
    animals.set_parameters(request.params)
    yield
    animals.set_parameters(animals.params)



def test_init():
    
    herb = Herbivores(5, 40)

    assert herb.age == 5
    assert herb.weight == 40