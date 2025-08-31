from django.contrib import admin
from .models import Contact, SuccessStory, StoryReaction, Question, Answer, QuestionUpvote, AnswerUpvote
from .models import FAQ

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'subject', 'created_at']
    list_filter = ['created_at']
    search_fields = ['first_name', 'last_name', 'email', 'subject']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )


@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'is_published', 'likes_count', 'created_at')
    list_filter = ('category', 'is_published', 'created_at')
    search_fields = ('title', 'content', 'user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('likes_count', 'hearts_count', 'celebrations_count', 'created_at', 'updated_at')
    list_editable = ('is_published',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Story Information', {
            'fields': ('user', 'title', 'content', 'category', 'tags')
        }),
        ('Publication', {
            'fields': ('is_published',)
        }),
        ('Statistics', {
            'fields': ('likes_count', 'hearts_count', 'celebrations_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(StoryReaction)
class StoryReactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'story', 'reaction_type', 'created_at')
    list_filter = ('reaction_type', 'created_at')
    search_fields = ('user__username', 'story__title')
    ordering = ('-created_at',)