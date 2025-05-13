from django.contrib import admin
from .models import UserComment

# Register the UserComment model in Django admin
@admin.register(UserComment)
class UserCommentAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('id', 'username', 'email', 'created_at', 'parent_comment', 'file_upload')

    # Enable filtering by date
    list_filter = ('created_at',)

    # Enable search by username, email, or comment text
    search_fields = ('username', 'email', 'text')

    # Make file upload field read-only
    readonly_fields = ('file_upload',)
