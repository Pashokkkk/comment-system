from django.contrib import admin
from .models import UserComment

# Register your models here.

@admin.register(UserComment)
class UserCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'created_at', 'parent_comment')
    list_filter = ('created_at',)
    search_fields = ('username', 'email', 'text')
