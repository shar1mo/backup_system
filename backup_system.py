import os
import time
import logging
import schedule
import subprocess

# Настройки
BACKUP_DIR = "/app/backups"
SOURCE_DIR = "/app/source"
LOG_FILE = "/app/backup.log"

# Настройка логирования
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Функция для выполнения полного бэкапа
def full_backup():
    backup_name = f"full_backup_{time.strftime('%Y%m%d_%H%M%S')}"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    logging.info(f"Начало полного бэкапа: {backup_name}")
    try:
        subprocess.run(["rsync", "-av", SOURCE_DIR, backup_path], check=True)
        logging.info(f"Полное бэкап успешно завершен: {backup_name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при выполнении полного бэкапа: {e}")

# Функция для выполнения инкрементального бэкапа
def incremental_backup():
    last_full_backup = get_last_full_backup()
    if not last_full_backup:
        logging.warning("Не найдено предыдущего полного бэкапа. Выполняется полное бэкап.")
        full_backup()
        return
    backup_name = f"incremental_backup_{time.strftime('%Y%m%d_%H%M%S')}"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    logging.info(f"Начало инкрементального бэкапа: {backup_name}")
    try:
        subprocess.run(["rsync", "-av", "--link-dest", last_full_backup, SOURCE_DIR, backup_path], check=True)
        logging.info(f"Инкрементальный бэкап успешно завершен: {backup_name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при выполнении инкрементального бэкапа: {e}")

# Функция для получения последнего полного бэкапа
def get_last_full_backup():
    backups = [os.path.join(BACKUP_DIR, d) for d in os.listdir(BACKUP_DIR) if d.startswith("full_backup_")]
    if backups:
        return max(backups, key=os.path.getctime)
    return None

# Функция для восстановления данных
def restore_backup(backup_name):
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    if not os.path.exists(backup_path):
        logging.error(f"Резервная копия {backup_name} не найдена.")
        return
    logging.info(f"Начало восстановления из резервной копии: {backup_name}")
    try:
        subprocess.run(["rsync", "-av", backup_path, SOURCE_DIR], check=True)
        logging.info(f"Восстановление успешно завершено: {backup_name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при восстановлении: {e}")

# Настройка расписания
def setup_schedule():
    schedule.every().day.at("00:00").do(full_backup)
    schedule.every().hour.do(incremental_backup)

# Основная функция
def main():
    setup_schedule()
    logging.info("Система бэкапа запущена.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()