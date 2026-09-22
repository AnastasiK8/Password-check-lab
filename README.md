![CI](https://github.com/AnastasiK8/Password-check-lab/actions/workflows/ci.yml/badge.svg)
# Password-check-lab

## Опис

Модуль `password_check.py` перевіряє надійність пароля: довжину, наявність цифр,
великих і малих літер. Автоматичні тести знаходяться у файлі `test_password_check.py`.

При кожному push і pull request у гілку `main` автоматично запускається CI
(`.github/workflows/ci.yml`), який встановлює залежності й запускає тести.