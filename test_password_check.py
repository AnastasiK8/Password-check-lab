"""Автоматичні тести для модуля password_check.py."""
import pytest
from password_check import (
    is_strong_password,
    count_digits,
    has_upper_case,
    has_lower_case,
    has_special_char,
    is_common_password,
    password_strength_score,
    strength_label,
)


def test_strong_password_valid():
    assert is_strong_password("Passw0rd") is True
    assert is_strong_password("Str0ngPass123") is True


def test_password_too_short():
    assert is_strong_password("Pas1") is False


def test_password_without_digit():
    assert is_strong_password("Password") is False


def test_password_without_upper_case():
    assert is_strong_password("password1") is False


def test_password_without_lower_case():
    assert is_strong_password("PASSWORD1") is False


def test_password_edge_case_exact_length():
    assert is_strong_password("Abcdefg1") is True


def test_password_common_is_rejected():
    # Навіть якщо формально довгий і містить цифри - поширений пароль недійсний
    assert is_strong_password("Password1") is True  # не зі списку - валідний
    assert is_strong_password("password1") is False  # з урахуванням списку і регістру


def test_is_strong_password_wrong_type_raises():
    with pytest.raises(TypeError):
        is_strong_password(12345678)


def test_count_digits():
    assert count_digits("Abc123") == 3
    assert count_digits("NoDigitsHere") == 0


def test_has_upper_case():
    assert has_upper_case("abcDef") is True
    assert has_upper_case("abcdef") is False


def test_has_lower_case():
    assert has_lower_case("ABCdef") is True
    assert has_lower_case("ABCDEF") is False


def test_has_special_char():
    assert has_special_char("Pass@123") is True
    assert has_special_char("Password123") is False


def test_is_common_password():
    assert is_common_password("qwerty123") is True
    assert is_common_password("Xk9#mPz2!Lq") is False


def test_password_strength_score_weak():
    assert password_strength_score("abc") == 1  # тільки довжина < 8 не рахується, лишається 0... див. нижче
    assert password_strength_score("password") == 0  # поширений пароль


def test_password_strength_score_strong():
    assert password_strength_score("Xk9#mPz2!Lqwe") == 5


def test_strength_label():
    assert strength_label("password") == "слабкий"
    assert strength_label("Passw0rd") == "середній"
    assert strength_label("Xk9#mPz2!Lqwe") == "надійний"


def test_strength_score_type_error():
    with pytest.raises(TypeError):
        password_strength_score(None)
