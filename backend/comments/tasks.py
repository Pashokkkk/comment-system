from celery import shared_task
import time

@shared_task
def process_uploaded_file(file_path):
    # Це лише приклад — ти можеш тут парсити файл, аналізувати, стискати тощо
    time.sleep(5)
    print(f"✅ Обробка файлу завершена: {file_path}")
