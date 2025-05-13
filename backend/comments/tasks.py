from celery import shared_task
import time
from django.core.mail import send_mail

@shared_task
def process_uploaded_file(file_path):
    # Simulate file processing
    time.sleep(5)
    print(f"✅ File processing completed: {file_path}")

@shared_task
def send_comment_email(user_email, comment_text):
    # Send email with comment content
    send_mail(
        subject="📝 New Comment Received",
        message=comment_text,
        from_email="admin@example.com",
        recipient_list=[user_email]
    )
