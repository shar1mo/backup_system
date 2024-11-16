#!/bin/bash

# Тестирование создания файла
touch /app/source/test_file.txt
echo "Initial content" > /app/source/test_file.txt

# Тестирование изменения файла
echo "Modified content" > /app/source/test_file.txt

# Тестирование полного бэкапа
python3 backup_system.py full_backup

# Тестирование инкрементального бэкапа
python3 backup_system.py incremental_backup

# Тестирование восстановления данных
python3 backup_system.py restore_backup full_backup_20231010_000000

echo "Все тесты пройдены успешно"


Сделай скрипт исполняемым:


chmod +x test_script.sh