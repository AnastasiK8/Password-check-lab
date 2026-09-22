"""Модуль перевірки надійності пароля"""

SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"

# Cписок поширених слабких паролів для перевірки
COMMON_PASSWORDS = {
    "password", "12345678", "qwerty123", "admin123",
    "password1", "11223344", "12345678", "111111"
}


def is_strong_password(p):
    """Перевіряє, чи є пароль надійним.

    Пароль вважається надійним, якщо одночасно виконуються умови:
    - довжина пароля не менше 8 символів;
    - містить хоча б одну цифру;
    - містить хоча б одну велику літеру;
    - містить хоча б одну малу літеру;
    - не входить до списку поширених слабких паролів.

    Повертає True, якщо пароль надійний, інакше False.
    Викликає TypeError, якщо на вхід подано не рядок.
    """
    if not isinstance(p, str):
        raise TypeError("Пароль має бути рядком (str)")

    if len(p) < 8:
        return False

    if p.lower() in COMMON_PASSWORDS:
        return False

    has_digit = any(ch.isdigit() for ch in p)
    has_upper = any(ch.isupper() for ch in p)
    has_lower = any(ch.islower() for ch in p)

    return has_digit and has_upper and has_lower


def count_digits(p):
    """Повертає кількість цифр у паролі."""
    return sum(1 for ch in p if ch.isdigit())


def has_upper_case(p):
    """Повертає True, якщо пароль містить хоча б одну велику літеру."""
    return any(ch.isupper() for ch in p)


def has_lower_case(p):
    """Повертає True, якщо пароль містить хоча б одну малу літеру."""
    return any(ch.islower() for ch in p)


def has_special_char(p):
    """Повертає True, якщо пароль містить хоча б один спеціальний символ."""
    return any(ch in SPECIAL_CHARS for ch in p)


def is_common_password(p):
    """Повертає True, якщо пароль входить до списку поширених слабких паролів."""
    return p.lower() in COMMON_PASSWORDS


def password_strength_score(p):
    """Обчислює бал надійності пароля від 0 до 5.

    Нараховує по одному балу за кожну виконану умову:
    довжина >= 8, довжина >= 12, наявність цифри,
    наявність великої літери, наявність спецсимволу.
    Якщо пароль входить до списку поширених - повертає 0 незалежно від інших умов.
    """
    if not isinstance(p, str):
        raise TypeError("Пароль має бути рядком (str)")

    if is_common_password(p):
        return 0

    score = 0
    if len(p) >= 8:
        score += 1
    if len(p) >= 12:
        score += 1
    if any(ch.isdigit() for ch in p):
        score += 1
    if any(ch.isupper() for ch in p):
        score += 1
    if has_special_char(p):
        score += 1

    return score


def strength_label(p):
    """Повертає текстову оцінку надійності пароля на основі password_strength_score.

    0-1 балів -> "слабкий"
    2-3 бали  -> "середній"
    4-5 балів -> "надійний"
    """
    score = password_strength_score(p)
    if score <= 1:
        return "слабкий"
    elif score <= 3:
        return "середній"
    else:
        return "надійний"
