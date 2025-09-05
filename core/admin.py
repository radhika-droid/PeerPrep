from django.contrib import admin
from .models import FAQ
from .models import Contact, SuccessStory, StoryReaction, Question, Answer, QuestionUpvote, AnswerUpvote,Goal,Milestone,StudySession,Achievement,UserStats,WeeklyGoal

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

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')

# Add these admin configurations to your core/admin.py file

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'priority', 'status', 'progress_percentage', 'target_date', 'is_completed', 'created_at')
    list_filter = ('category', 'priority', 'status', 'is_completed', 'created_at')
    search_fields = ('title', 'description', 'user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at', 'completed_at')
    list_editable = ('status', 'progress_percentage')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Goal Information', {
            'fields': ('user', 'title', 'description', 'category', 'priority')
        }),
        ('Progress', {
            'fields': ('status', 'progress_percentage', 'is_completed', 'target_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'goal', 'goal_user', 'is_completed', 'due_date', 'created_at')
    list_filter = ('is_completed', 'due_date', 'created_at')
    search_fields = ('title', 'description', 'goal__title', 'goal__user__username')
    readonly_fields = ('created_at', 'completed_at')
    list_editable = ('is_completed',)
    ordering = ('-created_at',)
    
    def goal_user(self, obj):
        return obj.goal.user.username
    goal_user.short_description = 'Goal Owner'
    
    fieldsets = (
        ('Milestone Information', {
            'fields': ('goal', 'title', 'description', 'due_date')
        }),
        ('Status', {
            'fields': ('is_completed',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'subject', 'duration_minutes', 'productivity_rating', 'date', 'created_at')
    list_filter = ('subject', 'date', 'productivity_rating', 'created_at')
    search_fields = ('title', 'description', 'notes', 'user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at',)
    ordering = ('-date', '-created_at')
    
    fieldsets = (
        ('Session Information', {
            'fields': ('user', 'subject', 'title', 'description', 'date')
        }),
        ('Performance', {
            'fields': ('duration_minutes', 'productivity_rating')
        }),
        ('Additional', {
            'fields': ('goals_related', 'notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'achievement_type', 'points', 'is_earned', 'earned_at')
    list_filter = ('achievement_type', 'is_earned', 'earned_at')
    search_fields = ('title', 'description', 'user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('earned_at',)
    list_editable = ('is_earned',)
    ordering = ('-earned_at',)
    
    fieldsets = (
        ('Achievement Information', {
            'fields': ('user', 'title', 'description', 'achievement_type', 'icon')
        }),
        ('Rewards', {
            'fields': ('points', 'is_earned', 'related_goal')
        }),
        ('Timestamps', {
            'fields': ('earned_at',)
        }),
    )

@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_study_hours', 'total_goals_completed', 'current_streak_days', 'achievement_points', 'last_activity_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-total_study_hours',)
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Study Statistics', {
            'fields': ('total_study_hours', 'current_streak_days', 'longest_streak_days', 'last_activity_date')
        }),
        ('Community Statistics', {
            'fields': ('total_questions_asked', 'total_answers_given', 'total_success_stories')
        }),
        ('Achievements', {
            'fields': ('total_goals_completed', 'achievement_points')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(WeeklyGoal)
class WeeklyGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'week_start', 'target_study_hours', 'actual_study_hours', 'target_sessions', 'actual_sessions', 'progress_percentage', 'is_completed')
    list_filter = ('week_start', 'is_completed', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'progress_percentage')
    ordering = ('-week_start',)
    
    def progress_percentage(self, obj):
        return f"{obj.progress_percentage():.1f}%"
    progress_percentage.short_description = 'Progress %'
    
    fieldsets = (
        ('Weekly Goal', {
            'fields': ('user', 'week_start')
        }),
        ('Targets', {
            'fields': ('target_study_hours', 'target_sessions')
        }),
        ('Actual Progress', {
            'fields': ('actual_study_hours', 'actual_sessions', 'is_completed')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )