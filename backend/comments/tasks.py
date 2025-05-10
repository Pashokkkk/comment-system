from celery import shared_task
import time

@shared_task
def process_uploaded_file(file_path):
    # Just an example
    time.sleep(5)
    print(f"✅ Обробка файлу завершена: {file_path}")
