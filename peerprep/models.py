from django.contrib import admin
from .models import (
    Profile, StudyNote, Question, Session, Message, 
    CodeSubmission, Note
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'experience_level']
    list_filter = ['experience_level']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'bio', 'skills']
    ordering = ['user__username']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Details', {
            'fields': ('bio', 'skills', 'experience_level')
        }),
    )


@admin.register(StudyNote)
class StudyNoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'uploader', 'upload_date']
    list_filter = ['subject', 'upload_date']
    search_fields = ['title', 'uploader__username']
    readonly_fields = ['upload_date']
    ordering = ['-upload_date']
    
    fieldsets = (
        ('Note Information', {
            'fields': ('title', 'subject', 'file')
        }),
        ('Upload Details', {
            'fields': ('uploader', 'upload_date')
        }),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'tags']
    list_filter = ['difficulty']
    search_fields = ['title', 'description', 'tags']
    ordering = ['difficulty', 'title']
    
    fieldsets = (
        ('Question Details', {
            'fields': ('title', 'description', 'difficulty', 'tags')
        }),
    )


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['question__title']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    filter_horizontal = ['participants']
    
    fieldsets = (
        ('Session Information', {
            'fields': ('question', 'is_active', 'participants')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'session', 'content_preview', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['sender__username', 'content']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Message Preview'
    
    fieldsets = (
        ('Message Details', {
            'fields': ('session', 'sender', 'content')
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        }),
    )


@admin.register(CodeSubmission)
class CodeSubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session', 'language', 'submitted_at']
    list_filter = ['language', 'submitted_at']
    search_fields = ['user__username', 'code']
    readonly_fields = ['submitted_at']
    ordering = ['-submitted_at']
    
    fieldsets = (
        ('Submission Details', {
            'fields': ('session', 'user', 'language')
        }),
        ('Code', {
            'fields': ('code',)
        }),
        ('Timestamp', {
            'fields': ('submitted_at',)
        }),
    )


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'uploader', 'upload_date']
    list_filter = ['subject', 'upload_date']
    search_fields = ['title', 'subject', 'uploader__username']
    readonly_fields = ['upload_date']
    ordering = ['-upload_date']
    
    fieldsets = (
        ('Note Information', {
            'fields': ('title', 'subject', 'file')
        }),
        ('Upload Details', {
            'fields': ('uploader', 'upload_date')
        }),
    )