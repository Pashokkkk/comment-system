from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os
from .tasks import process_uploaded_file

# Validate uploaded file based on extension, dimensions, and size
def validate_file(value):
    ext = os.path.splitext(value.name)[1].lower()

    if ext in ['.jpg', '.jpeg', '.png']:
        img = Image.open(value)
        if img.width > 320 or img.height > 240:
            pass  # Allow, will be resized if needed

    if ext in ['.txt', '.md']:
        if value.size > 100 * 1024:
            raise ValidationError("Maximum text file size is 100 KB.")

    return value

class UserComment(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    homepage_url = models.URLField(blank=True, null=True)
    text = models.TextField()
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    file_upload = models.FileField(
        upload_to='uploads/',
        blank=True,
        null=True,
        validators=[validate_file]
    )
    captcha_text = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        # Save comment to DB
        super().save(*args, **kwargs)

        # Run async task if file exists
        if self.file_upload and self.file_upload.name:
            from pathlib import Path
            full_path = Path(self.file_upload.path)
            if full_path.exists():
                process_uploaded_file.delay(str(full_path))

    def resize_image(self):
        # Resize uploaded image if too large
        img = Image.open(self.file_upload.path)

        if img.width > 320 or img.height > 240:
            img.thumbnail((320, 240))

            buffer = BytesIO()
            format = 'JPEG' if img.format == 'JPEG' else 'PNG'
            img.save(buffer, format=format)

            name = os.path.basename(self.file_upload.name)
            self.file_upload.save(name, ContentFile(buffer.getvalue()), save=False)
            buffer.close()

            # Save resized image
            super().save(update_fields=['file_upload'])

    def __str__(self):
        # String representation of comment
        return f"{self.username} ({self.created_at.date()})"
