![CI](https://github.com/AnastasiK8/Password-check-lab/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.13-blue)
![License](https://img.shields.io/badge/license-MIT-green)
# Password-check-lab

## Опис

Модуль `password_check.py` перевіряє надійність пароля: довжину, наявність цифр,
великих і малих літер. Автоматичні тести знаходяться у файлі `test_password_check.py`.

При кожному push і pull request у гілку `main` автоматично запускається CI
(`.github/workflows/ci.yml`), який встановлює залежності й запускає тести.