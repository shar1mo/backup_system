# Система автоматического бэкапа

## Установка и запуск

1. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/yourusername/backup_system.git
    cd backup_system
    ```

2. Соберите и запустите контейнер:

    ```bash
    ./build_and_run.sh
    ```

## Ручной запуск

1. Активируйте виртуальное окружение:

    ```bash
    source backup_system_env/bin/activate
    ```

2. Запустите скрипт для отслеживания изменений:

    ```bash
    python3 backup_system.py
    ```

## Тестирование

1. Запустите скрипт для автоматического тестирования:

    ```bash
    ./test_script.sh
    ```

## Зависимости

- Python 3.12
- schedule
- rsync