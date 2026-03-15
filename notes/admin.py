from django.contrib import admin
from .models import Note, Attachment


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'lead',
        'deal',
        'created_at',
    )

    search_fields = (
        'content',
    )


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = (
        'uploaded_by',
        'lead',
        'deal',
        'created_at',
    )










