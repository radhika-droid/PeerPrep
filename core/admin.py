from django.contrib import admin
from .models import (
    Contact, SuccessStory, StoryReaction, StudyNote,
    FAQ, Question, Answer, QuestionUpvote, AnswerUpvote,
    Goal, Milestone, StudySession, Achievement, UserStats, 
    WeeklyGoal, StudyProfile, StudyPartnerRequest, 
    StudyPartnership, PartnerStudySession
)


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


@admin.register(StudyNote)
class StudyNoteAdmin(admin.ModelAdmin):
    # FIXED: Added 'is_verified' to list_display
    list_display = ['title', 'subject', 'uploader', 'upload_date', 'is_approved', 'is_public', 'is_verified', 'download_count']
    list_filter = ['subject', 'is_approved', 'is_public', 'is_verified', 'upload_date']
    search_fields = ['title', 'topic', 'description', 'uploader__username']
    readonly_fields = ['upload_date', 'updated_at', 'download_count']
    list_editable = ['is_approved', 'is_public', 'is_verified']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'upvotes', 'views', 'is_solved', 'created_at')
    list_filter = ('is_solved', 'created_at')
    search_fields = ('title', 'content', 'user__username', 'tags')
    readonly_fields = ('created_at', 'updated_at', 'views', 'upvotes')
    list_editable = ('is_solved',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Question Information', {
            'fields': ('user', 'title', 'content', 'tags')
        }),
        ('Status', {
            'fields': ('is_solved',)
        }),
        ('Statistics', {
            'fields': ('upvotes', 'views'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question_title', 'user', 'is_accepted', 'upvotes', 'created_at')
    list_filter = ('is_accepted', 'created_at')
    search_fields = ('content', 'user__username', 'question__title')
    readonly_fields = ('created_at', 'updated_at', 'upvotes')
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
            'fields': ('upvotes',),
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


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'goal_type', 'target_hours', 'current_hours', 'is_completed', 'start_date', 'end_date')
    list_filter = ('goal_type', 'is_completed', 'start_date')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at',)
    list_editable = ('is_completed',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Goal Information', {
            'fields': ('user', 'title', 'description', 'goal_type')
        }),
        ('Progress', {
            'fields': ('target_hours', 'current_hours', 'is_completed', 'start_date', 'end_date')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'goal', 'is_completed', 'order')
    list_filter = ('is_completed',)
    search_fields = ('title', 'description', 'goal__title')
    list_editable = ('is_completed', 'order')
    ordering = ('order',)
    
    fieldsets = (
        ('Milestone Information', {
            'fields': ('goal', 'title', 'description', 'order')
        }),
        ('Status', {
            'fields': ('is_completed', 'completed_at')
        }),
    )


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'duration_minutes', 'date', 'created_at')
    list_filter = ('date', 'subject', 'created_at')
    search_fields = ('user__username', 'subject', 'notes')
    readonly_fields = ('created_at',)
    ordering = ('-date', '-created_at')
    
    fieldsets = (
        ('Session Information', {
            'fields': ('user', 'subject', 'duration_minutes', 'date')
        }),
        ('Additional', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'achievement_type', 'earned_at')
    list_filter = ('achievement_type', 'earned_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('earned_at',)
    ordering = ('-earned_at',)
    
    fieldsets = (
        ('Achievement Information', {
            'fields': ('user', 'title', 'description', 'achievement_type', 'icon')
        }),
        ('Timestamps', {
            'fields': ('earned_at',)
        }),
    )


@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_study_hours', 'total_sessions', 'current_streak', 'longest_streak', 'goals_completed')
    search_fields = ('user__username',)
    readonly_fields = ('updated_at',)
    ordering = ('-total_study_hours',)
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Study Statistics', {
            'fields': ('total_study_hours', 'total_sessions', 'current_streak', 'longest_streak', 'last_study_date')
        }),
        ('Goals', {
            'fields': ('goals_completed',)
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(WeeklyGoal)
class WeeklyGoalAdmin(admin.ModelAdmin):
    # FIXED: Removed non-existent fields (actual_study_hours, target_sessions, actual_sessions)
    # Using actual model fields: target_hours, current_hours
    list_display = ('user', 'week_start', 'target_hours', 'current_hours', 'is_completed')
    list_filter = ('week_start', 'is_completed', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)
    ordering = ('-week_start',)
    
    fieldsets = (
        ('Weekly Goal', {
            'fields': ('user', 'week_start')
        }),
        ('Progress', {
            'fields': ('target_hours', 'current_hours', 'is_completed')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(StudyProfile)
class StudyProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'study_level', 'created_at')
    list_filter = ('study_level', 'created_at')
    search_fields = ('user__username', 'subjects_of_interest', 'bio')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'bio', 'avatar')
        }),
        ('Study Preferences', {
            'fields': ('subjects_of_interest', 'study_level', 'study_goals', 'preferred_study_time')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(StudyPartnerRequest)
class StudyPartnerRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'created_at', 'responded_at')
    list_filter = ('status', 'created_at')
    search_fields = ('from_user__username', 'to_user__username', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Request Information', {
            'fields': ('from_user', 'to_user', 'message')
        }),
        ('Status', {
            'fields': ('status', 'responded_at')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )


@admin.register(StudyPartnership)
class StudyPartnershipAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user1__username', 'user2__username')
    readonly_fields = ('created_at',)
    list_editable = ('is_active',)
    ordering = ('-created_at',)


@admin.register(PartnerStudySession)
class PartnerStudySessionAdmin(admin.ModelAdmin):
    list_display = ('partnership', 'subject', 'duration_minutes', 'date', 'created_by')
    list_filter = ('subject', 'date', 'created_at')
    search_fields = ('subject', 'partnership__user1__username', 'partnership__user2__username')
    readonly_fields = ('created_at',)
    ordering = ('-date',)
    
    fieldsets = (
        ('Session Information', {
            'fields': ('partnership', 'subject', 'created_by', 'date')
        }),
        ('Details', {
            'fields': ('duration_minutes', 'notes')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )