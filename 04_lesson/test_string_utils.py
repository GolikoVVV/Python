import pytest
from string_utils import StringUtils

string_utils = StringUtils()

"""ПОЗИТИВНЫЙ ТЕСТ - Заглавная буква"""
@pytest.mark.parametrize("input_str, expected", [
    ("skypro", "Skypro"),
    ("123", "123"),
])
def test_capitalize_positive(input_str, expected):
    assert string_utils.capitalize(input_str) == expected

"""НЕГАТИВНЫЙ ТЕСТ - Заглавная буква"""
@pytest.mark.parametrize("input_str, expected", [
    ("123abc", "123abc"),
    ("", ""),
    ("   ", "   "),
    ("None", "None"),
])
def test_capitalize_negative(input_str, expected):
    assert string_utils.capitalize(input_str) == expected

"""ПОЗИТИВНЫЙ ТЕСТ - Пробел"""
@pytest.mark.parametrize("input_str, expected", [
    (" skypro", "skypro"),
    ("123", "123"),
    ("04 апреля 2023", "04 апреля 2023"),
])
def test_trim_positive(input_str, expected):
    assert string_utils.trim(input_str) == expected

"""НЕГАТИВНЫЙ ТЕСТ - Пробел"""
@pytest.mark.parametrize("input_str, expected", [
    ("123abc", "123abc"),
    ("", ""),
])
def test_trim_negative(input_str, expected):
    assert string_utils.trim(input_str) == expected

"""ПОЗИТИВНЫЙ ТЕСТ - Символ"""
@pytest.mark.parametrize("input_str, symbol", [
    ("skypro", "y"),
    ("123", "2"),
])
def test_contains_positive(input_str, symbol):
    assert string_utils.contains(input_str, symbol) == True

"""НЕГАТИВНЫЙ ТЕСТ - Символ"""
@pytest.mark.parametrize("input_str, symbol", [
    ("123abc", "Y"),
    ("", " "),
])
def test_contains_negative(input_str, symbol):
    assert string_utils.contains(input_str, symbol) == False

"""ПОЗИТИВНЫЙ ТЕСТ - Удаление символа"""
@pytest.mark.parametrize("input_str, symbol, expected", [
    ("skypro", "s", "kypro"),
    ("123", "123", ""),
])
def test_delete_symbol_positive(input_str, symbol, expected):
    assert string_utils.delete_symbol(input_str, symbol) == expected

"""НЕГАТИВНЫЙ ТЕСТ - Удаление символа"""
@pytest.mark.parametrize("input_str, symbol, expected", [
    ("123abc", "Y", "123abc"),
    ("", " ", ""),
])
def test_delete_symbol_negative(input_str, symbol, expected):
    assert string_utils.delete_symbol(input_str, symbol) == expected