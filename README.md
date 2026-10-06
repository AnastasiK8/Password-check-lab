![CI](https://github.com/AnastasiK8/Password-check-lab/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.13-blue)
![License](https://img.shields.io/badge/license-MIT-green)
# Password-check-lab

## Опис

Модуль `password_check.py` перевіряє надійність пароля: довжину, наявність цифр,
великих і малих літер. Автоматичні тести знаходяться у файлі `test_password_check.py`.

При кожному push і pull request у гілку `main` автоматично запускається CI
(`.github/workflows/ci.yml`), який встановлює залежності й запускає тести.

## Запуск через Docker

docker pull ghcr.io/anastasik8/ci-lab-app:latest
docker run --rm ghcr.io/anastasik8/ci-lab-app:latest

## Запуск через Docker Compose

docker compose up --build

## CI/CD-конвеєр

Source -> Build -> Test -> Package -> Deploy

При кожному push у гілку main автоматично: встановлюються залежності,
запускаються тести, збирається й публікується Docker-образ у GHCR,
після чого Terraform розгортає цей образ і перевіряє результат.