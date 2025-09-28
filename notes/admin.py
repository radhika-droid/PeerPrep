from django.contrib import admin
from .models import StudyNote, Note

@admin.register(StudyNote)
class StudyNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'get_uploader_name', 'upload_date')
    list_filter = ('subject', 'upload_date')
    search_fields = ('title', 'subject', 'uploader__username')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'uploader', 'upload_date')
    list_filter = ('subject', 'upload_date')
    search_fields = ('title', 'subject', 'uploader__username')
