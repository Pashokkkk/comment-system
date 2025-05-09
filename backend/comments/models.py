from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
import os
from .tasks import process_uploaded_file

def validate_file(value):
        # we get the extention here
        ext = os.path.splitext(value.name)[1].lower()

        # if it is an image check the size
        if ext in ['.jpg', '.jpeg', '.png']:
            img = Image.open(value)
            if img.width > 320 or img.height > 240:
                raise ValidationError("Максимальний розмір зображення — 320x240 пікселів.")

        # if it is a text file check the size
        if ext in ['.txt', '.md']:
            if value.size > 100 * 1024:
                raise ValidationError("Максимальний розмір текстового файлу — 100 KB.")

        return value

class UserComment(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()
    homepage_url = models.URLField(blank=True, null=True)
    text = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    file_upload = models.FileField(upload_to='uploads/', blank=True, null=True, validators=[validate_file])
    captcha_text = models.CharField(max_length=10)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file_upload:
            process_uploaded_file.delay(self.file_upload.path)


    def __str__(self):
        return f"{self.username} ({self.created_at.date()})"
    
    