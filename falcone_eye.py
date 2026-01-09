import os
import time
import shutil
from datetime import datetime

WATCH_FOLDERS = [
    r"C:\Users\Administrator\3D Objects",
    r"C:\Users\Administrator\Contacts",
    r"C:\Users\Administrator\Desktop",
    r"C:\Users\Administrator\Documents",
    r"C:\Users\Administrator\Downloads",
    r"C:\Users\Administrator\Favorites",
    r"C:\Users\Administrator\Links",
    r"C:\Users\Administrator\Music",
    r"C:\Users\Administrator\Pictures",
    r"C:\Users\Administrator\Saved Games",
    r"C:\Users\Administrator\Searches",
    r"C:\Users\Administrator\Videos",
]
BACKUP_ROOT = r"C:\Users\Falcone"
LOG_FILE = os.path.join(BACKUP_ROOT, "falcone_eye.log")

# интервал копирования
POLL_INTERVAL = 5

# расширения временных файлов, которые игнорируем
TEMP_EXT = {".part", ".tmp"}

def log(message: str):
    os.makedirs(BACKUP_ROOT, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def is_file_stable(path: str, delay: int = 3) -> bool:
    """
      Проверяет, что файл не меняет размер в течение delay секунд.
    """
    try:
        size1 = os.path.getsize(path)
        time.sleep(delay)
        size2 = os.path.getsize(path)
        return size1 == size2
    except FileNotFoundError:
        return False

def scan_and_backup():
    """
    Обходит все WATCH_FOLDERS, копирует файлы в BACKUP_ROOT, сохраняя структуру.
    Копирует только те файлы, которых ещё нет в бэкапе и которые стабильны.
    """
    for root in WATCH_FOLDERS:
        if not os.path.exists(root):
            continue  # если папки нет, то спокойно пропускаем

        for dirpath, dirnames, filenames in os.walk(root):
            for filename in filenames:
                # пропускаем временные/частичные файлы
                ext = os.path.splitext(filename)[1].lower()
                if ext in TEMP_EXT:
                    continue

                src_path = os.path.join(dirpath, filename)

                # путь относительно наблюдаемой папки
                rel_path = os.path.relpath(src_path, root)
                backup_dir = os.path.join(
                    BACKUP_ROOT,
                    os.path.basename(root),  # имя корневой папки (Desktop, Downloads и т.п.)
                    os.path.dirname(rel_path)
                )
                backup_path = os.path.join(backup_dir, os.path.basename(src_path))

                try:
                    # если копия уже есть, то пропускаем
                    if os.path.exists(backup_path):
                        continue

                    # проверяем, что файл "устаканился" и больше не растёт
                    if not is_file_stable(src_path, delay=3):
                        log(f"Файл ещё изменяется, пропускаю пока: {src_path}")
                        continue

                    os.makedirs(backup_dir, exist_ok=True)
                    shutil.copy2(src_path, backup_path)
                    log(f"Скопирован файл: {src_path} -> {backup_path}")
                except Exception as e:
                    log(f"Ошибка при копировании {src_path}: {e}")

def main():
    log("=== Запуск Falcone_eye ===")
    while True:
        try:
            scan_and_backup()
        except Exception as e:
            log(f"Глобальная ошибка: {e}")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()