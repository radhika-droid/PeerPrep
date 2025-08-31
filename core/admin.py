from django.contrib import admin
from .models import Contact, SuccessStory, StoryReaction, Question, Answer, QuestionUpvote, AnswerUpvote

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

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'subject', 'is_solved', 'upvotes_count', 'answers_count', 'created_at')
    list_filter = ('subject', 'is_solved', 'created_at')
    search_fields = ('title', 'description', 'user__username', 'user__first_name', 'user__last_name', 'tags')
    readonly_fields = ('upvotes_count', 'created_at', 'updated_at')
    list_editable = ('is_solved',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Question Information', {
            'fields': ('user', 'subject', 'title', 'description', 'tags')
        }),
        ('Status', {
            'fields': ('is_solved',)
        }),
        ('Statistics', {
            'fields': ('upvotes_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question_title', 'user', 'is_accepted', 'upvotes_count', 'created_at')
    list_filter = ('is_accepted', 'created_at', 'question__subject')
    search_fields = ('content', 'user__username', 'question__title')
    readonly_fields = ('upvotes_count', 'created_at', 'updated_at')
    list_editable = ('is_accepted',)
    ordering = ('-created_at',)
    
    def question_title(self, obj):
        return obj.question.title[:50] + '...' if len(obj.question.title) > 50 else obj.question.title
    question_title.short_description = 'Question'
    
    fieldsets = (
        ('Answer Information', {
            'fields': ('user', 'question', 'content')
        }),
        ('Status', {
            'fields': ('is_accepted',)
        }),
        ('Statistics', {
            'fields': ('upvotes_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(QuestionUpvote)
class QuestionUpvoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'question_title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'question__title')
    ordering = ('-created_at',)
    
    def question_title(self, obj):
        return obj.question.title[:50] + '...' if len(obj.question.title) > 50 else obj.question.title
    question_title.short_description = 'Question'

@admin.register(AnswerUpvote)
class AnswerUpvoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer_preview', 'answer_author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'answer__content', 'answer__user__username')
    ordering = ('-created_at',)
    
    def answer_preview(self, obj):
        return obj.answer.content[:50] + '...' if len(obj.answer.content) > 50 else obj.answer.content
    answer_preview.short_description = 'Answer Preview'
    
    def answer_author(self, obj):
        return obj.answer.user.username
    answer_author.short_description = 'Answer Author'