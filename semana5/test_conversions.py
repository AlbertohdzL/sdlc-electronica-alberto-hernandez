import pytest
from semana5.conversions import celsius_to_fahrenheit, fahrenheit_to_celsius


def test_celsius_to_fahrenheit_valid():
    assert celsius_to_fahrenheit(0.0) == 32.0
    assert celsius_to_fahrenheit(100.0) == 212.0
    assert celsius_to_fahrenheit(23.5) == 74.3


def test_celsius_to_fahrenheit_below_absolute_zero():
    with pytest.raises(ValueError, match="cero absoluto"):
        celsius_to_fahrenheit(-300.0)


def test_fahrenheit_to_celsius_valid():
    assert fahrenheit_to_celsius(32.0) == 0.0
    assert fahrenheit_to_celsius(212.0) == 100.0


def test_fahrenheit_to_celsius_below_absolute_zero():
    with pytest.raises(ValueError, match="cero absoluto"):
        fahrenheit_to_celsius(-500.0)